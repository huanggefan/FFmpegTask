<template>
    <div class="ListView">
        <el-collapse v-model="activeName" accordion>
            <el-collapse-item v-for="(task, index) in $data.task_list" :key="task.id" :title="`${index + 1} - ${task.name}`" :name="task.id">
                <div class="task-detail">
                    <el-progress text-inside :percentage="task.progress * 100"/>
                    <el-table :data="task.commands">
                        <el-table-column prop="command" label="命令">
                            <template slot-scope="scope">
                                <span class="table-command" :title="scope.row.command">{{ scope.row.command }}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="progress" label="进度" width="420" sortable>
                            <template slot-scope="scope">
                                <el-progress class="table-progress" text-inside :percentage="(scope.row.status === 'finish') ? 100 : scope.row.progress * 100"/>
                            </template>
                        </el-table-column>
                        <el-table-column prop="status" label="状态" width="120" sortable>
                            <template slot-scope="scope">
                                <el-tag type="info" v-if="scope.row.status === 'wait'" class="table-status">等待中</el-tag>
                                <el-tag type="warning" v-if="scope.row.status === 'process'" class="table-status">执行中</el-tag>
                                <el-tag type="success" v-if="scope.row.status === 'finish'" class="table-status">已完成</el-tag>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
import {api_task_list} from "@/api/task";

export default {
    name: `ListView`,
    data() {
        return {
            activeName: ``,
            task_list: [],
            interval: null
        }
    },
    methods: {
        async refresh_task_list() {
            this.$data.task_list = await api_task_list(this.onopen, this.onmessage, this.onerror)
        },
    },
    mounted() {
        this.refresh_task_list()
        this.$data.interval = setInterval(this.refresh_task_list, 1000 * 3)
    },
    async destroyed() {
        clearInterval(this.$data.interval)
        this.$data.interval = null
    },
}
</script>

<style scoped>

</style>

<style scoped>
.task-detail {
    padding: 0 0 0 48px;
}

.table-command {
    width: 100%;
    height: 32px;

    display: inline-block;

    word-break: keep-all;
    white-space: nowrap;
    overflow-x: hidden;
    text-overflow: ellipsis;

    font-size: 20px;
    line-height: 32px;
}

.table-progress {
    width: 100%;
    height: 32px;
}

.table-status {
    width: 100%;
    height: 32px;

    display: inline-block;

    text-align: center;
    font-size: 20px;
}

::v-deep .el-collapse-item__header {
    font-size: 24px;
    font-weight: bolder;
}
</style>
