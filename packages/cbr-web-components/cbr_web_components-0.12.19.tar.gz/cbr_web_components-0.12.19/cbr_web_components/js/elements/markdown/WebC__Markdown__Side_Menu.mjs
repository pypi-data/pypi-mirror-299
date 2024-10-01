import A                          from "../../core/A.mjs";
import Div                        from "../../core/Div.mjs";
import WebC__API_Markdown_To_Html from "../api/WebC__API_Markdown_To_Html.mjs";
import Load_Libraries__CSS from "../../utils/Load_Libraries__CSS.mjs";

export default class WebC__Markdown__Side_Menu extends WebC__API_Markdown_To_Html {

    static url__markdown__side_menu = 'en/web-site/home-page/side-menu.md'

  // base class methods overrides
    async connectedCallback() {
        super.connectedCallback();
    }

    async load_attributes() {
        super.load_attributes();
        this.content_path = this.getAttribute('content_path') || WebC__Markdown__Side_Menu.url__markdown__side_menu;
    }

    async setup() {
        await super.setup()
        await this.load_material_icons()
        await this.loadUserState();
        await this.loadMenuItems();
    }

  // class methods

    async load_material_icons() {
         this.css_load_result = await this.load_libraries__css.load_material_design()
    }
    async loadUserState() {
      this.userState = window.__USER_STATE__ || {                       // todo: for now user state is embedded in the page
        isLoggedIn: false,
        userGroups: [],
        username: null,
        adminToken: false,
        impersonating: false,
      };
    }

    async loadMenuItems() {
      this.menu_html     = this.markdown_html
      this.menu_metatada = this.markdown_metadata
    }

    async build() {
        this.renderMenu();
    }

    static class__side_menu           = 'side_menu_section';
    static class__side_menu_item      = 'side_menu_item';
    static class__side_menu_link      = 'side_menu_link';
    static class__side_menu_icon      = 'side_menu_icon';
    static class__side_menu_text      = 'side_menu_text';

    renderMenu() {
        const menu_data     = this.menu_data()
        const currentPath   = window.location.pathname;
        const div_side_menu = new Div({class: WebC__Markdown__Side_Menu.class__side_menu})
        for (const key in menu_data) {
            const item = menu_data[key];
            if (item.visibility !== true){
                continue }
            let class_icon            = `mdi me-2 ${item.icon} ${WebC__Markdown__Side_Menu.class__side_menu_icon}`
            let class__side_menu_item = WebC__Markdown__Side_Menu.class__side_menu_item
            let class__side_menu_link = WebC__Markdown__Side_Menu.class__side_menu_link

            if (currentPath.includes(item.href)) {
                class__side_menu_item += '_active'
                class__side_menu_link += '_active'              // hack to deal with current lack for support for nested css rules
            }
            const div_side_menu_item  = new Div({class: class__side_menu_item })
            const a_side_menu_link    = new A  ({class: class__side_menu_link, attributes: {href: item.href}})
            const i_side_menu_icon    = new Div({class: class_icon })
            const div_side_menu_text  = new Div({class: WebC__Markdown__Side_Menu.class__side_menu_text , value: item.text })
            a_side_menu_link  .add_elements(i_side_menu_icon, div_side_menu_text)
            div_side_menu_item.add_element (a_side_menu_link                    )
            div_side_menu     .add_element (div_side_menu_item                  )

        }
        this.set_inner_html(div_side_menu.html())
    }

    css_rules() {
        return {
            [`.${WebC__Markdown__Side_Menu.class__side_menu_section}`]: {
                'width': '220px', // Adjusted width
                'padding': '15px 10px',
                'background-color': '#f8f9fa',
                'border-right': '1px solid #ddd',
                'height': '100vh',
            },
            [`.${WebC__Markdown__Side_Menu.class__side_menu_item}`]: {
                'display': 'flex',
                'align-items': 'center',
                'padding': '8px 15px',                     // Adjusted padding for better spacing
                'margin': '5px 0',
                'cursor': 'pointer',
                'border-radius': '4px',
                //'transition': 'background 0.3s, color 0.3s',
            },
            [`.${WebC__Markdown__Side_Menu.class__side_menu_item}_active`]: {
                'display'         : 'flex',
                'align-items'     : 'center',
                'padding'         : '8px 15px',                     // Adjusted padding for better spacing
                'margin'          : '5px 0',
                'cursor'          : 'pointer',
                'border-radius'   : '10px',
                'background-color': '#26c6da',
            },
            [`.${WebC__Markdown__Side_Menu.class__side_menu_link}`]: {
                'display'        : 'flex',
                'align-items'    : 'center',
                'text-decoration': 'none',
                'color'          : '#96a5ac' ,
                'width'          : '100%',
                // '.active' : {                                            // todo: this need fix on Web_Component.create_stylesheet_from_css_rules()
                //     'background-color': 'red'
                // }
            },
            [`.${WebC__Markdown__Side_Menu.class__side_menu_link}_active`]: {       // short term hack to deal with prob with nested css rules
                'display'         : 'flex'   ,
                'align-items'     : 'center' ,
                'text-decoration' : 'none'   ,
                'color'           : '#FFFFFF',
                'width'           : '100%'   ,
            },
            [`.${WebC__Markdown__Side_Menu.class__side_menu_link}:hover`]: {
                'color': '#26c6da', // Text color changes to blue on hover
            },

            [`.${WebC__Markdown__Side_Menu.class__side_menu_icon}`]: {
                'font-size'   : '20px', // Adjust icon size
                'margin-right': '12px',
                //'color'       : '#a6b7bf'
            },
            [`.${WebC__Markdown__Side_Menu.class__side_menu_icon} .active`]: {
                'background-color': 'red'
            },
            [`.${WebC__Markdown__Side_Menu.class__side_menu_text}`]: {
                'font-size'      : '16px',
                'font-weight'    : '400',
            },
            [`.${WebC__Markdown__Side_Menu.class__side_menu_link} .active`]: {
                //'color': '#26c6da', // Active link text color
            },
            [`.${WebC__Markdown__Side_Menu.class__side_menu_item} .active`]: {
                //'background-color': '#e3f2fd', // Light blue background for active item
            }
        };
    }


    //todo: replace this with dynamic data
  menu_data() {
      return {
          'home'              : { 'href': 'home'                         , 'icon': 'mdi-home'                  , 'text': 'Home'                , 'logged_in': false , 'visibility': true                                                                    },
          'athena'            : { 'href': 'athena'                       , 'icon': 'mdi-robot'                 , 'text': 'Athena'              , 'logged_in': false , 'visibility': true                                                                    },
          'content'           : { 'href': 'content'                      , 'icon': 'mdi-security'              , 'text': 'Security content'    , 'logged_in': false , 'visibility': true                                                                    },
          'videos'            : { 'href': 'content/videos'               , 'icon': 'mdi-video'                 , 'text': 'Videos'              , 'logged_in': false , 'visibility': true                                                                    },
          'docs'              : { 'href': 'docs'                         , 'icon': 'mdi-book-multiple-variant' , 'text': 'Docs'                , 'logged_in': false , 'visibility': true                                                                    },
          'profile'           : { 'href': 'user/profile'                 , 'icon': 'mdi-account-check'         , 'text': 'Profile'             , 'logged_in': true  , 'visibility': 'config.LOGIN_ENABLED'                                                  },
          'dev'               : { 'href': 'dev'                          , 'icon': 'mdi-developer-board'       , 'text': 'Dev'                 , 'logged_in': true  , 'visibility': "g.user_groups and 'CBR-Team' in g.user_groups"                         },
          'minerva'           : { 'href': 'minerva'                      , 'icon': 'mdi-robot'                 , 'text': 'Minerva'             , 'logged_in': true  , 'visibility': "g.user_groups and 'CBR-Team' in g.user_groups"                         },
          'logout'            : { 'href': 'sign-out'                     , 'icon': 'mdi-logout'                , 'text': 'Logout'              , 'logged_in': true  , 'visibility': "current_user.get('username')"                                          },
          'login'             : { 'href': 'login'                        , 'icon': 'mdi-login'                 , 'text': 'Login'               , 'logged_in': true  , 'visibility': "config.LOGIN_ENABLED and not current_user.get('username')"             },
          'restore_admin_user': { 'href': 'admin/restore_admin_user'     , 'icon': 'mdi-restore'               , 'text': 'RESTORE ADMIN USER'  , 'logged_in': true  , 'visibility': "current_user.get('admin_token') and current_user.get('impersonating')" },
          'chat_with_llms'    : { 'href': 'chat-with-llms'               , 'icon': 'mdi-message'               , 'text': 'Chat with LLMs'      , 'logged_in': false , 'visibility': true                                                                    },
          'community_discord' : { 'href': 'https://discord.gg/HdJJbFpzMX', 'icon': 'mdi-message'               , 'text': 'Community (Discord)' , 'logged_in': false , 'visibility': true                                                                    }
      };
  }
}

WebC__Markdown__Side_Menu.define()
