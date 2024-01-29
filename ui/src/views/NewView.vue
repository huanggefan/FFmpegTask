<template>
    <div class="NewView">
        <el-divider class="divider">基本信息</el-divider>

        <el-form>
            <el-form-item label="任务名">
                <el-input v-model="$data.form.name"/>
            </el-form-item>
            <el-form-item label="源文件夹">
                <el-input v-model="$data.form.src_folder"/>
            </el-form-item>
            <el-form-item label="输出文件夹">
                <el-input v-model="$data.form.out_folder"/>
            </el-form-item>
            <el-form-item label="视频">
                <DirectoryChoose :ext="'video/*'" v-model="$data.form.src_videos"/>
            </el-form-item>
            <el-form-item label="字幕">
                <DirectoryChoose :ext="'.ass,.srt'" v-model="$data.form.src_subtitles"/>
            </el-form-item>
        </el-form>

        <el-divider class="divider">视频详情</el-divider>

        <el-table stripe fit :data="$data.table">
            <el-table-column prop="target" label="输出文件名">
                <template slot-scope="scope">
                    <span>{{ scope.row.target_name }}.mkv</span>
                </template>
            </el-table-column>
            <el-table-column prop="video" label="源视频文件"/>
            <el-table-column prop="subtitle" label="字幕文件">
                <template slot-scope="scope">
                    <div v-for="(item, index) in scope.row.subtitle" :key="index">
                        <SubtitleFileChoose :value="item.subtitle" @input="choose_subtitle_file(scope.$index, index, $event)"/>
                    </div>
                </template>
            </el-table-column>
            <el-table-column prop="audios" label="音频轨道">
                <template slot-scope="scope">
                    <div v-for="(item, index) in scope.row.stream_audios" :key="index">
                        <AudioStreamChoose :value="item" @input="choose_audio_stream(scope.$index, index, $event)"/>
                    </div>
                </template>
            </el-table-column>
            <el-table-column prop="subtitles" label="字幕轨道">
                <template slot-scope="scope">
                    <div v-for="(item, index) in scope.row.stream_subtitles" :key="index">
                        <SubtitleStreamChoose :value="item" @input="choose_subtitle_stream(scope.$index, index, $event)"/>
                    </div>
                </template>
            </el-table-column>
        </el-table>

        <el-divider class="divider">FFMPEG 命令</el-divider>

        <el-table stripe fit :data="$data.commands">
            <el-table-column prop="src_video" label="源视频">
                <template slot-scope="scope">
                    <span class="command-table-src-out-file" :title="scope.row.src_video">{{ scope.row.src_video }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="out_video" label="输出视频">
                <template slot-scope="scope">
                    <span class="command-table-src-out-file" :title="scope.row.out_video">{{ scope.row.out_video }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="command" label="命令">
                <template slot-scope="scope">
                    <span class="command-table-command" :title="scope.row.command">{{ scope.row.command }}</span>
                </template>
            </el-table-column>
        </el-table>

        <el-divider class="divider">操作</el-divider>

        <el-button type="primary" @click="parse_task">解析</el-button>
        <el-button type="primary" @click="gen_command">命令生成</el-button>
        <el-button type="primary" @click="submit_task">提交</el-button>
    </div>
</template>

<script>
import {api_gen_command, api_parse_task, api_submit_task} from "@/api/task";
import DirectoryChoose from "@/components/DirectoryChoose";
import AudioStreamChoose from "@/components/AudioStreamChoose";
import SubtitleStreamChoose from "@/components/SubtitleStreamChoose";
import SubtitleFileChoose from "@/components/SubtitleFileChoose";
import FileBrowser from "@/components/FileBrowser";

export default {
    name: `HomeView`,
    components: {FileBrowser, SubtitleFileChoose, SubtitleStreamChoose, AudioStreamChoose, DirectoryChoose},
    data() {
        return {
            form: {
                name: ``,
                src_folder: ``,
                out_folder: ``,
                src_videos: [],
                src_subtitles: [],
            },
            table: [],
            commands: [],
        }
    },
    methods: {
        async parse_task() {
            const resp = await api_parse_task(this.$data.form.src_folder, this.$data.form.src_videos, this.$data.form.src_subtitles)

            this.$data.table.splice(0, this.$data.table.length)

            let file_index = 0

            for (let item of resp) {
                const subtitle_list = []
                for (let subtitle_file of item.subtitle_file) {
                    const u = {
                        subtitle: subtitle_file,
                        choose: false,
                    }
                    subtitle_list.push(u)
                }

                const obj = {
                    target_name: `${file_index}`,
                    video: item.video_file,
                    subtitle: subtitle_list,
                    stream_audios: item.info.audio_streams,
                    stream_subtitles: item.info.subtitle_streams,
                }
                this.$data.table.push(obj)

                file_index++
            }

            if (this.$data.form.out_folder === ``) {
                this.$data.form.out_folder = this.$data.form.src_folder + `_out`
            }

            this.$message.success(`任务解析成功`)
        },
        async gen_command() {
            const item_list = []

            for (let item of this.$data.table) {
                const obj = {
                    input_file: item.video,
                    input_subtitle_files: [],
                    output_file: item.target_name,
                    choose_video_streams: [0],
                    choose_audio_streams: [],
                    choose_subtitle_streams: [],
                }
                for (let file of item.subtitle) {
                    if (file.choose) {
                        obj.input_subtitle_files.push(file.subtitle)
                    }
                }
                for (let index = 0; index < item.stream_audios.length; index++) {
                    if (item.stream_audios[index].choose) {
                        obj.choose_audio_streams.push(index)
                    }
                }
                for (let index = 0; index < item.stream_subtitles.length; index++) {
                    if (item.stream_subtitles[index].choose) {
                        obj.choose_subtitle_streams.push(index)
                    }
                }
                item_list.push(obj)
            }

            this.$data.commands = await api_gen_command(this.$data.form.src_folder, this.$data.form.out_folder, item_list)

            this.$message.success(`命令生成成功`)
        },
        async submit_task() {
            const video_src_list = []
            const video_dist_list = []
            const commands = []

            for (let c of this.$data.commands) {
                video_src_list.push(c.src_video)
                video_dist_list.push(c.out_video)
                commands.push(c.command)
            }

            await api_submit_task(
                this.$data.form.name,
                this.$data.form.src_folder,
                this.$data.form.out_folder,
                video_src_list,
                video_dist_list,
                commands
            )

            this.$message.success(`任务提交成功`)
            this.reset()
        },

        reset() {
            this.$data.form = {
                name: ``,
                src_folder: ``,
                out_folder: ``,
                src_videos: [],
                src_subtitles: [],
            }
            this.$data.table = []
            this.$data.commands = []
        },

        choose_subtitle_file(file_index, subtitle_file_index, event) {
            this.$data.table[file_index].subtitle[subtitle_file_index].choose = event
        },
        choose_audio_stream(file_index, audio_index, event) {
            this.$data.table[file_index].stream_audios[audio_index].choose = event
        },
        choose_subtitle_stream(file_index, subtitle_index, event) {
            this.$data.table[file_index].stream_subtitles[subtitle_index].choose = event
        }
    },
}
</script>

<style scoped>
.divider {
    width: 100%;
    height: 4px;

    margin: 128px 0 16px 0;
}

.divider:first-child {
    margin: 0 0 16px 0;
}
</style>

<style scoped>
.command-table-src-out-file {
    width: 100%;

    display: inline-block;

    word-break: keep-all;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.command-table-command {
    width: 100%;

    display: inline-block;

    word-break: keep-all;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
