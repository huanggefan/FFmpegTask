import request from "@/utils/request";

export async function api_parse_task(src_folder, video_files, subtitle_files) {
    const url = `/api/parse_task`
    const payload = {
        src_folder: src_folder,
        video_files: video_files,
        subtitle_files: subtitle_files,
    }

    return await request.post(
        url,
        payload,
        {}
    )
}

export async function api_gen_command(src_folder, out_folder, item_list) {
    const url = `/api/gen_command`

    const payload = {
        src_folder: src_folder,
        out_folder: out_folder,
        item_list: item_list,
    }

    return await request.post(
        url,
        payload,
        {}
    )
}

export async function api_submit_task(name, src, dist, video_src_list, video_dist_list, commands) {
    const url = `/api/submit_task`

    const payload = {
        name: name,
        src: src,
        dist: dist,
        video_src_list: video_src_list,
        video_dist_list: video_dist_list,
        commands: commands,
    }

    return await request.post(
        url,
        payload,
        {}
    )
}

export async function api_task_list() {
    const url = `/api/task_list`

    return await request.get(
        url,
        {}
    )
}

export async function sse_task_list(onopen, onmessage, onerror) {
    const url = `/sse/task_list`

    const event_source = new EventSource(url)

    event_source.onopen = (event) => {
        onopen(event)
    }
    event_source.onmessage = (event) => {
        onmessage(event)
    }
    event_source.onerror = (error) => {
        onerror(error)
    }

    return event_source
}