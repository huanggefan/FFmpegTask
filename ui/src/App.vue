<template>
    <div class="App" @contextmenu.prevent.stop="() => {return false}">
        <el-menu :default-active="$data.defaultActive" mode="horizontal" router class="menu">
            <el-menu-item index="/new">新建任务</el-menu-item>
            <el-menu-item index="/list">任务列表</el-menu-item>
        </el-menu>

        <router-view class="wrapper"/>
    </div>
</template>

<script>
export default {
    name: `App`,
    data() {
        return {
            defaultActive: `/new`,
        }
    },
    methods: {},
    mounted() {
        this.$router.replace(`/new`)
    },
}
</script>

<style scoped>
.App {
    width: 100%;
    height: 100%;

    margin: 0;
    padding: 16px;

    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-content: flex-start;
}

.menu {
    width: 100%;
    height: 64px;

    margin: 0 0 64px 0;
}

.wrapper {
    width: 100%;
    height: auto;
    flex-grow: 1;
}
</style>
