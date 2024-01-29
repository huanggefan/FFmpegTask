<template>
    <div class="SubtitleStreamChoose">
        <el-checkbox v-model="$data.choose" class="choose"/>
        <span :title="stream_title" class="title">{{ stream_title }}</span>
    </div>
</template>

<script>
export default {
    name: `SubtitleStreamChoose`,
    props: {
        value: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            choose: false,
        }
    },
    computed: {
        duration() {
            return `${this.$props.value.duration_hour}:${this.$props.value.duration_minute}:${this.$props.value.duration_second}.${this.$props.value.duration_microsecond}`
        },
        stream_title() {
            return `${this.$props.value.codec_long_name} ${this.duration}`
        },
    },
    watch: {
        "$data.choose": {
            handler(val) {
                this.$emit(`input`, val)
            },
            immediate: true,
            deep: true,
        },
    },
}
</script>

<style scoped>
.SubtitleStreamChoose {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-content: center;

    margin: 2px 0 2px 0;
}

.choose {
    margin: 0 22px 0 0;

    width: 24px;
    height: 24px;

    font-size: 24px;
    line-height: 24px;

    display: flex;
    flex-direction: row;
    justify-content: center;
    align-content: center;
}

.title {
    width: 500px;
    height: 24px;

    font-size: 24px;
    line-height: 24px;

    display: inline-block;

    overflow: hidden;
    text-overflow: ellipsis;
    word-break: keep-all;
    white-space: nowrap;
}
</style>