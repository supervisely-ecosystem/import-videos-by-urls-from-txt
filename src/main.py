import os
import requests
import supervisely as sly
import workflow as w

TEAM_ID = int(os.environ["context.teamId"])
WORKSPACE_ID = int(os.environ["context.workspaceId"])
INPUT_FILE = os.environ.get("modal.state.slyFile")
PROJECT_ID = None
PROJECT_NAME = None
DATASET_NAME = None

IMPORT_MODE = os.environ["modal.state.importMode"]

if IMPORT_MODE == "new":
    PROJECT_NAME = os.environ.get("modal.state.projectName")

if IMPORT_MODE == "project":
    PROJECT_ID = os.environ.get("modal.state.inputProjectId")
    DATASET_NAME = os.environ.get("modal.state.datasets")

if IMPORT_MODE == "dataset":
    PROJECT_ID = os.environ.get("modal.state.inputProjectId")
    DATASET_NAME = os.environ.get("modal.state.datasets")

my_app = sly.AppService(ignore_task_id=True)


def download_file(url, local_path, logger, cur_video_index, total_videos_count):
    headers = {"User-Agent": "Mozilla/5.0"}
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        total_size_in_bytes = int(r.headers.get("content-length", 0))
        progress = sly.Progress(
            "Downloading [{}/{}] {!r}".format(
                cur_video_index, total_videos_count, sly.fs.get_file_name_with_ext(local_path)
            ),
            total_size_in_bytes,
            ext_logger=logger,
            is_size=True,
        )
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                progress.iters_done_report(len(chunk))
    return local_path


@my_app.callback("import_videos")
@sly.timeit
def import_videos(api: sly.Api, task_id, context, state, app_logger):
    local_file = os.path.join(my_app.data_dir, sly.fs.get_file_name_with_ext(INPUT_FILE))
    api.file.download(TEAM_ID, INPUT_FILE, local_file)

    with open(local_file) as f:
        video_urls = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    video_urls = [x.strip() for x in video_urls]

    if IMPORT_MODE == "new":
        project_name = PROJECT_NAME if PROJECT_NAME else "my-project"
        project = api.project.create(
            WORKSPACE_ID, project_name, type=sly.ProjectType.VIDEOS, change_name_if_conflict=True
        )
        dataset = api.dataset.create(project.id, "ds0")
        w.workflow_output(api, project.id, type="project")
    elif IMPORT_MODE == "project":
        project = api.project.get_info_by_id(PROJECT_ID)
        dataset_name = DATASET_NAME if DATASET_NAME else "ds0"
        dataset = api.dataset.get_info_by_name(project.id, dataset_name)
        if dataset is None:
            dataset = api.dataset.create(project.id, dataset_name)
        w.workflow_output(api, project.id, type="project")
    elif IMPORT_MODE == "dataset":
        project = api.project.get_info_by_id(PROJECT_ID)
        dataset_name = DATASET_NAME if DATASET_NAME else "ds0"
        dataset = api.dataset.get_info_by_name(project.id, dataset_name)
        if dataset is None:
            dataset = api.dataset.create(project.id, dataset_name)
        w.workflow_output(api, dataset.id, type="dataset")
    for idx, video_url in enumerate(video_urls):
        try:
            app_logger.info("Processing [{}/{}]: {!r}".format(idx, len(video_urls), video_url))
            video_name = sly.fs.get_file_name_with_ext(video_url)
            local_video_path = os.path.join(my_app.data_dir, video_name)
            download_file(video_url, local_video_path, app_logger, idx + 1, len(video_urls))
            item_name = api.video.get_free_name(
                dataset.id, video_name
            )  # checks if item with the same name exists in dataset
            api.video.upload_paths(dataset.id, [item_name], [local_video_path])
        except Exception as e:
            app_logger.warn(f"Error during import {video_url}: {repr(e)}")
        finally:
            if sly.fs.file_exists(local_video_path):
                sly.fs.silent_remove(local_video_path)

    api.task.set_output_project(task_id, project.id, project.name)
    my_app.stop()


def main():
    sly.logger.info(
        "Script arguments",
        extra={
            "TEAM_ID": TEAM_ID,
            "WORKSPACE_ID": WORKSPACE_ID,
            "INPUT_FILE": INPUT_FILE,
            "PROJECT_NAME": PROJECT_NAME,
        },
    )
    my_app.run(initial_events=[{"command": "import_videos"}])


if __name__ == "__main__":
    sly.main_wrapper("main", main)
