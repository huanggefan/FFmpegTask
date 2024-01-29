<template>
    <div class="SubtitleFileChoose">
        <el-checkbox v-model="$data.choose" class="choose"/>
        <span :title=" $props.value" class="title">{{ $props.value }}</span>
    </div>
</template>

<script>
export default {
    name: `SubtitleFileChoose`,
    props: {
        value: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            choose: false,
        }
    },
    computed: {
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
.SubtitleFileChoose {
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