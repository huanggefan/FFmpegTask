<template>
    <div class="FileBrowser">
        <el-input :value="choose_tips" placeholder="路径" readonly clearable @click.native.stop="open_choose"/>

        <el-dialog title="文件浏览器" :visible.sync="$data.dialog"
                   class="choose"
                   :close-on-click-modal="false"
                   :close-on-press-escape="false"
                   :show-close="false"
                   :destroy-on-close="true">
            <div class="choose-path">{{ path_stack }}</div>
            <div class="choose-bar">
                <el-input placeholder="在当前目录搜索" prefix-icon="el-icon-search" v-model="$data.query.name" clearable/>
            </div>
            <div class="choose-wrapper">
                <div v-for="(item, index) in $data.node.folder"
                     :class="{ active: $data.choose.folder.includes(item) }"
                     :key="`folder-${index}`" :title="item"
                     @click="choose_folder(item)"
                     @contextmenu.prevent.stop="enter_folder(item)">
                    <i class="el-icon-folder"/>
                    <span>{{ item }}</span>
                </div>
                <div v-for="(item, index) in $data.node.file"
                     v-show="$props.can_file"
                     :class="{ active: $data.choose.file.includes(item) }"
                     :key="`file-${index}`" :title="item"
                     @click="choose_file(item)">
                    <i class="el-icon-document"/>
                    <span>{{ item }}</span>
                </div>
            </div>
            <div slot="footer">
                <el-button type="primary" @click="submit_choose">确 定</el-button>
                <el-button @click="close_choose">取消</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
export default {
    name: `FileBrowser`,
    props: {
        api: {
            type: String,
            required: false,
            default: `/api/path`,
        },
        value: {
            type: Object,
            required: false,
            default: null,
        },
        can_directory: {
            type: Boolean,
            required: false,
            default: true,
        },
        can_file: {
            type: Boolean,
            required: false,
            default: true,
        },
    },
    data() {
        return {
            dialog: false,
            loading: false,

            stack: [],

            node: {
                folder: [
                    `a`, `b`, `c`, `d`, `e`,
                    `aaaa`, `bbbb`, `cccc`, `dddd`, `eeee`,
                ],
                file: [
                    `a.txt`, `b.json`, `c.c`, `d.py`, `e.java`,
                    `a.mkv`, `b.mp4`, `c.avi`, `d.mov`, `e.mkv`,
                    `a.mp3`, `b.flac`, `c.egg`, `d.mp3`, `e.mp3`,
                    `a.jpg`, `b.jpeg`, `c.png`, `d.bmp`, `e.gif`,
                ],
            },

            query: {
                name: ``,
            },

            choose: {
                folder: [],
                file: [],
            },
        }
    },
    methods: {
        open_choose() {
            this.$data.dialog = true
        },
        close_choose() {
            this.$data.dialog = false
            this.$data.choose.folder = []
            this.$data.choose.file = []
        },
        submit_choose() {

        },

        choose_folder(item) {
            if (!this.$props.can_directory) {
                return
            }

            if (!this.$data.choose.folder.includes(item)) {
                this.$data.choose.folder.push(item)
            } else {
                const i = this.$data.choose.folder.indexOf(item)
                this.$data.choose.folder.splice(i, 1)
            }
        },
        choose_file(item) {
            if (!this.$props.can_file) {
                return
            }

            if (!this.$data.choose.file.includes(item)) {
                this.$data.choose.file.push(item)
            } else {
                const i = this.$data.choose.file.indexOf(item)
                this.$data.choose.file.splice(i, 1)
            }
        },

        enter_folder(item) {
            console.log(item)
            return false
        },
    },
    computed: {
        path_stack() {
            return `/`
        },
        choose_tips() {
            return `文件夹：${this.$data.choose.folder.length}，文件：${this.$data.choose.file.length}`
        }
    },
}
</script>

<style scoped>

</style>

<style scoped>

</style>

<style scoped>
.choose {

}

.choose ::v-deep > .el-dialog {
    width: 1600px;
}

.choose .choose-path {
    margin: 0 0 12px 0;
}

.choose .choose-bar {
    margin: 0 0 12px 0;
}

.choose .choose-wrapper {
    display: grid;
    grid-template-rows: auto;
    grid-template-columns: repeat(10, 1fr);
    grid-gap: 16px 16px;
}

.choose .choose-wrapper > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    width: 141px;
    height: 141px;

    color: #2c3e50;

    border-width: 1px;
    border-radius: 2px;
    border-style: solid;
    border-color: #8c939d;
}

.choose .choose-wrapper > div:hover {
    cursor: pointer;
    color: #3a8ee6;
    border-color: #21a5f4;
}

.choose .choose-wrapper > div.active {
    color: #12c315;
    border-color: #12c315;
}

.choose .choose-wrapper > div > i {
}

.choose .choose-wrapper > div > span {
}
</style>