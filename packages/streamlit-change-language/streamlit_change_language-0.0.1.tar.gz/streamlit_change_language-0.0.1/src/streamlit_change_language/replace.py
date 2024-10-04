from enum import Enum


class Replace(Enum):
    # 上传
    file_uploader=[
        {'''["Drag and drop file",t?"s":""," here"]''':'''["请在这里拖放文件", t ? "s" : ""]'''},
        {'Limit ${m(s,g.Byte,0)} per file':'每个文件限制 ${m(s,g.Byte,0)} '},
        {'Browse files':'浏览文件'},
    ]
    # 日历
    date_input=[
        {
            '''["January","February","March","April","May","June","July","August","September","October","November","December"]'''
            :
                '''["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]'''
        },
        {
            '''["Su","Mo","Tu","We","Th","Fr","Sa"]'''
            :
                '''["周日","周一","周二","周三","周四","周五","周六"]'''
        },
        {
            '''["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]'''
            :
            '''["星期日","星期一","星期二","星期三","星期四","星期五","星期六"]'''
        }
    ]
    # 下拉框
    multiselect=[
        {'''"No results"''':'''"无选项"'''}
    ]
    multiselect_py=[
        {'''"Choose an option"''':'''"选择一个选项"'''}
    ]
    main=[
        {'''children:"Running..."''':'''children:"运行中..."'''},
        {'''"Stopping...":"Stop"''':'''"Stopping...":"停止"'''},
        {'''"Source file changed:"''':'''"源文件已发生改变."'''},
        {'''"Rerun"''':'''"重新运行"'''},
        {'''"Always rerun"''':'''"总是重新运行"'''},
        {'''"Connecting"''':'''"正在连接服务器"'''},
        {'''"Connecting to Streamlit server"''':'''"连接到应用所在的服务器"'''},
        {'''"Connection error"''':'''"连接失败"'''},
        {
            '''"Is Streamlit still running? If you accidentally stopped Streamlit, just restart it in your terminal:"'''
            :
                '''"Streamlit还在运行吗? 如果你不小心停止了Streamlit, 只需在终端中重新启动它:"'''
        },
        {'''"Deploy"''':'''"部署"'''},
        {'''"Deploy this app"''':'''"部署这个应用程序"'''},
        {'''"Streamlit Community Cloud"''':'''"Streamlit 社区云"'''},
        {'''"For the community"''':'''"可以在社区应用"'''},
        {'''"Deploy unlimited public apps for free"''':'''"可以免费部署公共应用程序且无数量的限制"'''},
        {'''"Apps are discoverable through the Streamlit gallery and search engines"''':'''"可以在Streamlit展示馆和搜索引擎上找到应用程序"'''},
        {'''"Deploy now"''':'''"开始部署"'''},
        {'''"Read more"''':'''"详细介绍"'''},
        {'''"Custom deployment"''':'''"自定义部署"'''},
        {'''"For companies"''':'''"可以在企业应用"'''},
        {'''"Deploy on your own hardware or in the cloud, with Docker, Kubernetes, etc"''':'''"可以使用Docker,Kubernetes等容器部署在你自己的硬件或云上"'''},
        {'''"Set up your own authentication"''':'''"可以设置您自己的身份验证"'''},
        {'''"Unable to deploy"''':'''"无法部署"'''},
        {
            '''"The app\\u2019s code is not connected to a remote GitHub repository. To deploy on Streamlit Community Cloud, please put your code in a GitHub repository and publish the current branch. Read more in"'''
            :
                '''"这个应用程序的代码没有连接到远程GitHub存储库.要在Streamlit社区云上部署，请将您的代码放在GitHub存储库中并发布当前分支."'''
        },
        {'''"our documentation"''':'''"在我们的文档上阅读详细介绍"'''},
        {'''"Try again"''':'''"重试"'''},
        {'''"Continue anyway":"Close"''':'''"Continue anyway":"关闭"'''},


        {'''label:"Settings"''':'''label:"设置"'''},

        {'''children:"Settings"''':'''children:"设置"'''},
        {'''"Development"''':'''"开发"'''},
        {'''"Run on save"''':'''"自动保存运行"'''},
        {'''"Automatically updates the app when the underlying code is updated."''':'''"当源代码更新时自动更新应用程序."'''},
        {'''"Appearance"''':'''"外观"'''},
        {'''"Wide mode"''':'''"宽屏模式"'''},
        {'''"Turn on to make this app occupy the entire width of the screen"''':'''"打开使这个应用程序占据整个屏幕的宽度"'''},
        {'''"Choose app theme, colors and fonts"''':'''"选择应用程序的主题，颜色和字体"'''},
        {'''"Use system setting"''':'''"使用系统设置"'''},
        {'''"Light"''':'''"明亮模式"'''},
        {'''"Dark"''':'''"暗黑模式"'''},
        {'''"Edit active theme"''':'''"编辑当前主题"'''},
        {
            '''"Changes made to the active theme will exist for the duration of a session. To discard changes and recover the original theme, refresh the page."'''
            :
            '''"对当前主题所做的更改将只存在于此次会话期间.若要放弃更改并恢复初始主题，请刷新页面."'''
        },
        {'''"Primary color"''':'''"主题颜色"'''},
        {'''"Primary accent color for interactive elements."''':'''"交互元素的主要强调颜色."'''},
        {'''"Background color for the main content area."''': '''"主内容区的背景颜色."'''},
        {'''"Background color"''':'''"背景颜色"'''},
        {'''"Text color"''':'''"文本颜色"'''},
        {'''"Color used for almost all text."''':'''"用于几乎所有文本的颜色."'''},
        {'''"Secondary background color"''':'''"次要背景颜色"'''},
        {'''"Background color used for the sidebar and most interactive widgets."''':'''"侧边栏和大多数交互式小组件的背景颜色."'''},
        {'''"Font family for all text in the app, except code blocks."''': '''"应用中除了代码块外的所有文本的字体."'''},
        {'''"Font family"''':'''"字体"'''},
        {
            '''"To save your changes, copy your custom theme into the clipboard and paste it into the"'''
            :
            '''"要保存更改,请点击下方按钮将自定义主题复制到剪贴板中,将其粘贴到"'''
        },
        {'''" section of your"''':'''" 下面,文件:"'''},
        {'''" file."''':'''" 中."'''},
        {'''"Copy theme to clipboard"''':'''"将主题复制到剪贴板"'''},
        {'''"Copied to clipboard "''':'''"复制成功 "'''},
        {'''label:"Print"''':'''label:"打印"'''},

        {'''"Record a screencast"''':'''"录制屏幕"'''},
        {
            '''"This will record a video with the contents of your screen, so you can easily share what you're seeing with others."'''
            :
            '''"在这里可以将你屏幕上的内容录制成视频，这样你就可以很容易的将你所看到的分享给他人."'''
        },
        {'''"Also record audio"''':'''"同时录制音频"'''},
        {'''"Press "''':'''"按下 "'''},
        {'''" any time to stop recording."''':'''" 随时停止录制."'''},
        {'''"Start recording!"''':'''"开始录制!"'''},
        {
            '''"Due to limitations with some browsers, this feature is only supported on recent desktop versions of Chrome, Firefox, and Edge."'''
            :
                '''"由于某些浏览器的限制,该功能仅支持最新的桌面版Chrome,Firefox和Edge."'''
        },

        {'''"About"''':'''"关于"'''},
        {'''"Made with"''':'''"鸣谢!"'''},
        {'''"Developer options"''':'''"开发人员选项"'''},
        {'''"Clear caches"''':'''"清除缓存"'''},
        {'''"Clear cache"''':'''"清除缓存"'''},
        {'''"Are you sure you want to clear the app's function caches?"''':'''"您确定要清除应用的函数缓存吗?"'''},
        {'''"This will remove all cached entries from functions using"''':'''"这将从这些函数中删除所有缓存项:"'''},
        {'''" and "''': '''" 和 "'''},
        {'''"Cancel"''':'''"取消"'''}

    ]

    @staticmethod
    def get_js_value(module:str):
        if module == 'file_uploader':
            return Replace.file_uploader.value
        elif module == 'date_input':
            return Replace.date_input.value
        elif module == 'multiselect':
            return Replace.multiselect.value
        elif module == 'multiselect_py':
            return Replace.multiselect_py.value
        elif module == 'main':
            return Replace.main.value

    @staticmethod
    def get_py_value(module: str):
        if module == 'multiselect':
            return Replace.multiselect_py.value