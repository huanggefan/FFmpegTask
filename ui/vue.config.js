module.exports = {
    publicPath: ``,
    outputDir: `../data/ui`,
    assetsDir: ``,
    indexPath: `index.html`,

    /******************************************************************************/

    lintOnSave: false,
    runtimeCompiler: false,
    productionSourceMap: true,
    filenameHashing: true,

    /******************************************************************************/

    pages: {
        index: {
            entry: `src/main.js`,
            template: `public/index.html`,
            filename: `index.html`,
            title: `FFMPEG Task`,
            chunks: [`chunk-vendors`, `chunk-common`, `index`]
        }
    },

    /******************************************************************************/

    devServer: {
        host: `127.0.0.1`,
        port: 8887,
        allowedHosts: [`all`],
        proxy: {
            "/api": {
                target: `http://127.0.0.1:8888`,
                changeOrigin: true,
                ws: true,
                keepalive: false,
            },
        },
        compress: false,
    },
}
