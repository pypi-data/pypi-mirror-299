import argparse
import os
import time
from string import Template

import yaml
from clarifai_grpc.grpc.api import resources_pb2, service_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from google.protobuf import json_format
from rich import print

from clarifai.client import BaseClient
from clarifai.runners.utils.loader import HuggingFaceLoarder
from clarifai.utils.logging import logger


def _clear_line(n: int = 1) -> None:
  LINE_UP = '\033[1A'  # Move cursor up one line
  LINE_CLEAR = '\x1b[2K'  # Clear the entire line
  for _ in range(n):
    print(LINE_UP, end=LINE_CLEAR, flush=True)


class ModelUploader:
  DEFAULT_PYTHON_VERSION = 3.11
  CONCEPTS_REQUIRED_MODEL_TYPE = [
      'visual-classifier', 'visual-detector', 'visual-segmenter', 'text-classifier'
  ]

  def __init__(self, folder: str):
    self._client = None
    self.folder = self._validate_folder(folder)
    self.config = self._load_config(os.path.join(self.folder, 'config.yaml'))
    self.model_proto = self._get_model_proto()
    self.model_id = self.model_proto.id
    self.inference_compute_info = self._get_inference_compute_info()
    self.is_v3 = True  # Do model build for v3

  @staticmethod
  def _validate_folder(folder):
    if not folder.startswith("/"):
      folder = os.path.join(os.getcwd(), folder)
    logger.info(f"Validating folder: {folder}")
    if not os.path.exists(folder):
      raise FileNotFoundError(f"Folder {folder} not found, please provide a valid folder path")
    files = os.listdir(folder)
    assert "requirements.txt" in files, "requirements.txt not found in the folder"
    assert "config.yaml" in files, "config.yaml not found in the folder"
    assert "1" in files, "Subfolder '1' not found in the folder"
    subfolder_files = os.listdir(os.path.join(folder, '1'))
    assert 'model.py' in subfolder_files, "model.py not found in the folder"
    return folder

  @staticmethod
  def _load_config(config_file: str):
    with open(config_file, 'r') as file:
      config = yaml.safe_load(file)
    return config

  @property
  def client(self):
    if self._client is None:
      assert "model" in self.config, "model info not found in the config file"
      model = self.config.get('model')
      assert "user_id" in model, "user_id not found in the config file"
      assert "app_id" in model, "app_id not found in the config file"
      user_id = model.get('user_id')
      app_id = model.get('app_id')

      base = os.environ.get('CLARIFAI_API_BASE', 'https://api-dev.clarifai.com')

      self._client = BaseClient(user_id=user_id, app_id=app_id, base=base)
      logger.info(f"Client initialized for user {user_id} and app {app_id}")
    return self._client

  def _get_model_proto(self):
    assert "model" in self.config, "model info not found in the config file"
    model = self.config.get('model')

    assert "model_type_id" in model, "model_type_id not found in the config file"
    assert "id" in model, "model_id not found in the config file"
    assert "user_id" in model, "user_id not found in the config file"
    assert "app_id" in model, "app_id not found in the config file"

    model_proto = json_format.ParseDict(model, resources_pb2.Model())
    assert model_proto.id == model_proto.id.lower(), "Model ID must be lowercase"
    assert model_proto.user_id == model_proto.user_id.lower(), "User ID must be lowercase"
    assert model_proto.app_id == model_proto.app_id.lower(), "App ID must be lowercase"

    return model_proto

  def _get_inference_compute_info(self):
    assert ("inference_compute_info" in self.config
           ), "inference_compute_info not found in the config file"
    inference_compute_info = self.config.get('inference_compute_info')
    return json_format.ParseDict(inference_compute_info, resources_pb2.ComputeInfo())

  def maybe_create_model(self):
    resp = self.client.STUB.GetModel(
        service_pb2.GetModelRequest(
            user_app_id=self.client.user_app_id, model_id=self.model_proto.id))
    if resp.status.code == status_code_pb2.SUCCESS:
      logger.info(
          f"Model '{self.client.user_app_id.user_id}/{self.client.user_app_id.app_id}/models/{self.model_proto.id}' already exists, "
          f"will create a new version for it.")
      return resp

    request = service_pb2.PostModelsRequest(
        user_app_id=self.client.user_app_id,
        models=[self.model_proto],
    )
    return self.client.STUB.PostModels(request)

  def create_dockerfile(self):
    num_accelerators = self.inference_compute_info.num_accelerators
    if num_accelerators:
      dockerfile_template = os.path.join(
          os.path.dirname(os.path.dirname(__file__)),
          'dockerfile_template',
          'Dockerfile.cuda.template',
      )
    else:
      dockerfile_template = os.path.join(
          os.path.dirname(os.path.dirname(__file__)), 'dockerfile_template',
          'Dockerfile.cpu.template')

    with open(dockerfile_template, 'r') as template_file:
      dockerfile_template = template_file.read()

    dockerfile_template = Template(dockerfile_template)

    # Get the Python version from the config file
    build_info = self.config.get('build_info', {})
    if 'python_version' in build_info:
      python_version = build_info['python_version']
      logger.info(
          f"Using Python version {python_version} from the config file to build the Dockerfile")
    else:
      logger.info(
          f"Python version not found in the config file, using default Python version: {self.DEFAULT_PYTHON_VERSION}"
      )
      python_version = self.DEFAULT_PYTHON_VERSION

    # Replace placeholders with actual values
    dockerfile_content = dockerfile_template.safe_substitute(
        PYTHON_VERSION=python_version,
        name='main',
    )

    # Write Dockerfile
    with open(os.path.join(self.folder, 'Dockerfile'), 'w') as dockerfile:
      dockerfile.write(dockerfile_content)

  def download_checkpoints(self):
    if not self.config.get("checkpoints"):
      logger.info("No checkpoints specified in the config file")
      return

    assert "type" in self.config.get("checkpoints"), "No loader type specified in the config file"
    loader_type = self.config.get("checkpoints").get("type")
    if not loader_type:
      logger.info("No loader type specified in the config file for checkpoints")
    assert loader_type == "huggingface", "Only huggingface loader supported for now"
    if loader_type == "huggingface":
      assert "repo_id" in self.config.get("checkpoints"), "No repo_id specified in the config file"
      repo_id = self.config.get("checkpoints").get("repo_id")

      # prefer env var for HF_TOKEN but if not provided then use the one from config.yaml if any.
      if 'HF_TOKEN' in os.environ:
        hf_token = os.environ['HF_TOKEN']
      else:
        hf_token = self.config.get("checkpoints").get("hf_token", None)
        assert hf_token != 'hf_token', "The default 'hf_token' is not valid. Please provide a valid token or leave that field out of config.yaml if not needed."
      loader = HuggingFaceLoarder(repo_id=repo_id, token=hf_token)

      checkpoint_path = os.path.join(self.folder, '1', 'checkpoints')
      success = loader.download_checkpoints(checkpoint_path)

      if not success:
        logger.error(f"Failed to download checkpoints for model {repo_id}")
        return
      logger.info(f"Downloaded checkpoints for model {repo_id}")

  def _concepts_protos_from_concepts(self, concepts):
    concept_protos = []
    for concept in concepts:
      concept_protos.append(resources_pb2.Concept(
          id=str(concept[0]),
          name=concept[1],
      ))
    return concept_protos

  def hf_labels_to_config(self, labels, config_file):
    with open(config_file, 'r') as file:
      config = yaml.safe_load(file)
    model = config.get('model')
    model_type_id = model.get('model_type_id')
    assert model_type_id in self.CONCEPTS_REQUIRED_MODEL_TYPE, f"Model type {model_type_id} not supported for concepts"
    concept_protos = self._concepts_protos_from_concepts(labels)

    config['concepts'] = [{'id': concept.id, 'name': concept.name} for concept in concept_protos]

    with open(config_file, 'w') as file:
      yaml.dump(config, file, sort_keys=False)
    concepts = config.get('concepts')
    logger.info(f"Updated config.yaml with {len(concepts)} concepts.")

  def _get_model_version_proto(self):

    model_version = resources_pb2.ModelVersion(
        pretrained_model_config=resources_pb2.PretrainedModelConfig(),
        inference_compute_info=self.inference_compute_info,
    )

    model_type_id = self.config.get('model').get('model_type_id')
    if model_type_id in self.CONCEPTS_REQUIRED_MODEL_TYPE:

      loader = HuggingFaceLoarder()
      checkpoint_path = os.path.join(self.folder, '1', 'checkpoints')
      labels = loader.fetch_labels(checkpoint_path)
      # sort the concepts by id and then update the config file
      labels = sorted(labels.items(), key=lambda x: int(x[0]))

      config_file = os.path.join(self.folder, 'config.yaml')
      self.hf_labels_to_config(labels, config_file)

      model_version.output_info.data.concepts.extend(self._concepts_protos_from_concepts(labels))
    return model_version

  def upload_model_version(self):
    file_path = f"{self.folder}.tar.gz"
    logger.info(f"Will tar it into file: {file_path}")

    # Tar the folder
    os.system(f"tar --exclude=*~ -czvf {self.folder}.tar.gz -C {self.folder} .")
    logger.info("Tarring complete, about to start upload.")

    model_version = self._get_model_version_proto()

    response = self.maybe_create_model()

    for response in self.client.STUB.PostModelVersionsUpload(
        self.model_version_stream_upload_iterator(model_version, file_path),):
      percent_completed = 0
      if response.status.code == status_code_pb2.UPLOAD_IN_PROGRESS:
        percent_completed = response.status.percent_completed
      details = response.status.details

      _clear_line()
      print(
          f"Status: {response.status.description}, "
          f"Progress: {percent_completed}% - {details} ",
          f"request_id: {response.status.req_id}",
          end='\r',
          flush=True)
    print()
    if response.status.code != status_code_pb2.MODEL_BUILDING:
      logger.error(f"Failed to upload model version: {response.status.description}")
      return
    model_version_id = response.model_version_id
    logger.info(f"Created Model Version ID: {model_version_id}")

    self.monitor_model_build(model_version_id)

  def model_version_stream_upload_iterator(self, model_version, file_path):
    yield self.init_upload_model_version(model_version, file_path)
    with open(file_path, "rb") as f:
      file_size = os.path.getsize(file_path)
      chunk_size = int(127 * 1024 * 1024)  # 127MB chunk size
      num_chunks = (file_size // chunk_size) + 1
      logger.info("Uploading file...")
      logger.info("File size: ", file_size)
      logger.info("Chunk size: ", chunk_size)
      logger.info("Number of chunks: ", num_chunks)
      read_so_far = 0
      for part_id in range(num_chunks):
        try:
          chunk_size = min(chunk_size, file_size - read_so_far)
          chunk = f.read(chunk_size)
          if not chunk:
            break
          read_so_far += len(chunk)
          yield service_pb2.PostModelVersionsUploadRequest(
              content_part=resources_pb2.UploadContentPart(
                  data=chunk,
                  part_number=part_id + 1,
                  range_start=read_so_far,
              ))
        except Exception as e:
          logger.exception(f"\nError uploading file: {e}")
          break

    if read_so_far == file_size:
      logger.info("\nUpload complete!, waiting for model build...")

  def init_upload_model_version(self, model_version, file_path):
    file_size = os.path.getsize(file_path)
    logger.info(f"Uploading model version '{model_version.id}' of model {self.model_proto.id}")
    logger.info(f"Using file '{os.path.basename(file_path)}' of size: {file_size} bytes")
    return service_pb2.PostModelVersionsUploadRequest(
        upload_config=service_pb2.PostModelVersionsUploadConfig(
            user_app_id=self.client.user_app_id,
            model_id=self.model_proto.id,
            model_version=model_version,
            total_size=file_size,
            is_v3=self.is_v3,
        ))

  def monitor_model_build(self, model_version_id):
    st = time.time()
    while True:
      resp = self.client.STUB.GetModelVersion(
          service_pb2.GetModelVersionRequest(
              user_app_id=self.client.user_app_id,
              model_id=self.model_proto.id,
              version_id=model_version_id,
          ))
      status_code = resp.model_version.status.code
      if status_code == status_code_pb2.MODEL_BUILDING:
        logger.info(
            f"Model is building... (elapsed {time.time() - st:.1f}s)", end='\r', flush=True)
        time.sleep(1)
      elif status_code == status_code_pb2.MODEL_TRAINED:
        logger.info("\nModel build complete!")
        logger.info(
            f"Check out the model at https://clarifai.com/{self.client.user_app_id.user_id}/apps/{self.client.user_app_id.app_id}/models/{self.model_id}/versions/{model_version_id}"
        )
        break
      else:
        logger.info(
            f"\nModel build failed with status: {resp.model_version.status} and response {resp}")
        break


def main(folder, download_checkpoints):
  uploader = ModelUploader(folder)
  if download_checkpoints:
    uploader.download_checkpoints()
  uploader.create_dockerfile()
  input("Press Enter to continue...")
  uploader.upload_model_version()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--model_path', type=str, help='Path of the model folder to upload', required=True)
  # flag to default to not download checkpoints
  parser.add_argument(
      '--download_checkpoints',
      action='store_true',
      help=
      'Flag to download checkpoints before uploading and including them in the tar file that is uploaded. Defaults to False, which will attempt to download them at docker build time.',
  )
  args = parser.parse_args()

  main(args.model_path, args.download_checkpoints)
