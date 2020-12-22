import os
import supervisely_lib as sly

TEAM_ID = int(os.environ['context.teamId'])
WORKSPACE_ID = int(os.environ['context.workspaceId'])
INPUT_FILE = os.environ.get("modal.state.slyFile")
PROJECT_NAME = os.environ['modal.state.projectName']

my_app = sly.AppService()

PROJECT_ID = None
CLASSES = []
COLOR_INS = True
FONT = cv2.FONT_HERSHEY_COMPLEX


def download_file(url, local_path, logger):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        progress = sly.Progress("Downloading {!r}".format(sly.fs.get_file_name_with_ext(local_path)),
                                total_size_in_bytes, ext_logger=logger, is_size=True)
        with open(local_path, 'wb') as f:
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

    for video_url in video_urls:
        try:
            video_name = sly.fs.get_file_name_with_ext(video_url)
            local_video_path = os.path.join(my_app.data_dir, video_name)
            #download_file(video_url, local_video_path, app_logger)
        except Exception as e:
            app_logger.warn(f"Error during upload {video_name}: {repr(r)}")
        finally:
            sly.fs.silent_remove(local_video_path)

    my_app.stop()


def main():
    sly.logger.info("Script arguments", extra={
        "TEAM_ID": TEAM_ID,
        "WORKSPACE_ID": WORKSPACE_ID,
        "INPUT_FILE": INPUT_FILE,
        "PROJECT_NAME": PROJECT_NAME,
    })
    my_app.run(initial_events=[{"command": "import_videos"}])


if __name__ == "__main__":
    sly.main_wrapper("main", main)