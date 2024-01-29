module.exports = {
    "plugins": {
        "autoprefixer": {},
        'postcss-pxtorem': {
            rootValue: 256, // 256 代表 2560px 的屏幕
            unitPrecision: 3, // 保留 rem 小数点3位
            propList: [`*`], // 可以从 px 更改为 rem 的属性
            selectorBlackList: [], // 对 css 选择器进行过滤的数组，支持正则写法。
            replace: true,
            mediaQuery: false, // 媒体查询( @media screen 之类的)中不生效
            minPixelValue: 2, // px 小于 3 的不会被转换

            // eslint-disable-next-line no-unused-vars
            exclude: (file) => {
                return false
            },
        }
    }
}