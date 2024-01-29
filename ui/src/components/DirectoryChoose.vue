<template>
    <div class="DirectoryChoose">
        <el-input :value="files_str" readonly>
            <template slot="prepend">
                <input ref="path" type="file" :accept="$props.ext" multiple @change="getChoose($event)" style="display: none">
                <el-button @click.native="clickChoose($event)">选择</el-button>
            </template>
        </el-input>
    </div>
</template>

<script>
export default {
    name: `DirectoryChoose`,
    props: {
        value: {
            type: Array,
            required: true,
        },
        ext: {
            type: String,
            required: false,
            default: `*/*`,
        },
    },
    data() {
        return {
            files: [],
        }
    },
    methods: {
        clickChoose() {
            this.$refs.path.click()
        },
        getChoose(event) {
            const result = []
            for (let file of event.target.files) {
                result.push(file.name)
            }
            this.$data.files = result
        }
    },
    watch: {
        "$props.value": {
            handler(val, old_val) {
                if (old_val === undefined) {
                    return
                }

                const val_str = val.join(`,`)
                const old_val_str = old_val.join(`,`)
                if (val_str === old_val_str) {
                    return
                }

                this.$data.files = val
            },
            immediate: true,
            deep: true,
        },
        "$data.files": {
            handler(val, old_val) {
                if (old_val === undefined) {
                    return
                }

                const val_str = val.join(`,`)
                const old_val_str = old_val.join(`,`)
                if (val_str === old_val_str) {
                    return
                }

                this.$emit(`input`, val)
            },
            immediate: true,
            deep: true,
        },
    },
    computed: {
        files_str() {
            const total = `Total: ${this.$data.files.length}`
            const str = this.$data.files.join(`, `)
            return `${total}: ${str}`
        },
    },
}
</script>

<style scoped>
.DirectoryChoose {
}
</style>