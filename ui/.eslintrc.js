module.exports = {
    root: true,
    parserOptions: {
        ecmaVersion: 2020,
        sourceType: `module`
    },
    env: {
        browser: true,
        node: true,
        es6: true,
    },
    extends: [`plugin:vue/essential`, `eslint:recommended`],
    rules: {
        'no-tabs': `warn`, // 禁用 tab
        'no-mixed-spaces-and-tabs': `warn`, // 禁止空格和 tab 的混合缩进
        'no-var': `warn`, // 要求使用 let 或 const 而不是 var
        'no-duplicate-imports': `warn`, // 禁止重复模块导入
        'no-await-in-loop': `warn`, // 禁止在循环中出现 await
        'no-unreachable': `warn`, // 禁止在 return、throw、continue 和 break 语句之后出现不可达代码
        'no-unsafe-negation': `warn`, // 禁止对关系运算符的左操作数使用否定操作符
        'no-cond-assign': `warn`, // 禁止在条件语句中出现赋值操作符
        'no-extra-semi': `warn`, // 禁用不必要的分号
        'indent': [ // 缩进
            `warn`,
            4,
            {'SwitchCase': 2}
        ],
        'key-spacing': [ // 强制在对象字面量的属性中键和值之间使用一致的间距
            `warn`,
            {'beforeColon': false, 'afterColon': true}
        ],
        'keyword-spacing': [ // 强制在关键字前后使用一致的空格
            `warn`,
            {'before': true, 'after': true}
        ],
        'semi-spacing': [ // 强制分号之前和之后使用一致的空格
            `warn`,
            {'before': false, 'after': true}
        ],
        'arrow-body-style': [ // 要求箭头函数体使用大括号
            `warn`,
            `always`
        ],
        'arrow-parens': [ // 要求箭头函数的参数使用圆括号
            `warn`,
            `always`
        ],
        'quotes': [ // 强制使用一致的反勾号、双引号或单引号
            `warn`,
            `backtick`
        ],
        'no-console': [ // 禁用 console
            `warn`,
            {'allow': [`warn`, `error`]}
        ],
        'vue/no-async-in-computed-properties': `warn`, // disallow asynchronous actions in computed properties
        'vue/require-v-for-key': `warn`, // require v-bind:key with v-for directives
        'vue/html-end-tags': `warn`, // enforce end tag style
        'vue/singleline-html-element-content-newline': [ // require a line break before and after the contents of a singleline element
            `off`,
            {
                'ignoreWhenNoAttributes': true,
                'ignoreWhenEmpty': true,
                'ignores': [`pre`, `textarea`, `p`]
            }
        ],
        'vue/multiline-html-element-content-newline': [ // require a line break before and after the contents of a multiline element
            `warn`, {
                'ignoreWhenEmpty': true,
                'ignores': [`pre`, `textarea`, `p`],
                'allowEmptyLines': false
            }
        ],
        'vue/html-indent': [ // enforce consistent indentation in <template>
            `warn`,
            4,
            {
                'attribute': 1,
                'baseIndent': 1,
                'closeBracket': 0,
                'alignAttributesVertically': true,
                'ignores': []
            }
        ],
        'vue/html-quotes': [ //  enforce quotes style of HTML attributes
            `warn`,
            `double`,
            {'avoidEscape': false}
        ],
        'vue/html-self-closing': [ // enforce self-closing style
            `warn`,
            {
                'html': {'void': `never`, 'normal': `always`, 'component': `always`},
                'svg': `always`,
                'math': `always`
            }
        ],
        'vue/no-unused-components': [ // disallow registering components that are not used inside templates
            `warn`,
            {
                'ignoreWhenBindingPresent': true
            }
        ],
        'vue/html-closing-bracket-spacing': [
            `warn`,
            {
                'startTag': `never`,
                'endTag': `never`,
                'selfClosingTag': `never`
            }
        ],
        'vue/max-attributes-per-line': [
            `warn`,
            {
                'singleline': {'max': 8},
                'multiline': {'max': 8}
            }
        ]

    }
}
