import Web_Component from "../../core/Web_Component.mjs";
import API__Invoke   from "../../data/API__Invoke.mjs";
import Div           from "../../core/Div.mjs";

export default class WebC__API_Markdown_To_Html extends Web_Component {
    static url__api_markdown_file_to_html_and_metadata = '/markdown/render/markdown-file-to-html-and-metadata?path='
    static class__markdown_section                     = 'markdown_section'
    static class__markdown_html                        = 'markdown_html'
    static class__markdown_metadata                    = 'markdown_metadata'
    static class__markdown_error                       = 'markdown_error'
    static class__markdown_title                       = 'markdown_title'
    static class__markdown_sub_title                   = 'markdown_sub_title'
    static class__markdown_description                 = 'markdown_description'
    static on_error_return_value                       = { html:'(error loading markdown content)', metadata:{}}

    constructor() {
        super();
    }

    // base class methods overrides
    async connectedCallback() {
        super.connectedCallback()
        await this.setup()
        await this.build()
        this.raise_event('build-complete')

    }

    load_attributes() {
        super.load_attributes()
        this.content_path  = this.getAttribute('content_path')
    }

    // class methods

    async build() {
        const div_markdown    = new Div({class: WebC__API_Markdown_To_Html.class__markdown_section     })
        const div_html        = new Div({class: WebC__API_Markdown_To_Html.class__markdown_html        })
        const div_metadata    = new Div({class: WebC__API_Markdown_To_Html.class__markdown_metadata    })
        const div_error       = new Div({class: WebC__API_Markdown_To_Html.class__markdown_error       })
        const div_title       = new Div({class: WebC__API_Markdown_To_Html.class__markdown_title       })
        const div_sub_title   = new Div({class: WebC__API_Markdown_To_Html.class__markdown_sub_title   })
        const div_description = new Div({class: WebC__API_Markdown_To_Html.class__markdown_description })


        div_html.value      = this.markdown_html
        if (this.markdown_metadata) {
            div_error      .value = this.markdown_metadata.error
            div_title      .value = this.markdown_metadata.title
            div_sub_title  .value = this.markdown_metadata.sub_title
            div_description.value = this.markdown_metadata.description

            if (this.markdown_metadata.error      ) { div_metadata.add_element(div_error      ) }
            if (this.markdown_metadata.title      ) { div_metadata.add_element(div_title      ) }
            if (this.markdown_metadata.sub_title  ) { div_metadata.add_element(div_sub_title  ) }
            if (this.markdown_metadata.description) { div_metadata.add_element(div_description) }

            div_markdown.add_element(div_metadata)
        }
        div_markdown.add_element(div_html)

        const html         = div_markdown.html()
        this.set_inner_html(html)
        this.add_css_rules(this.css_rules())
    }

    css_rules() {
        return {
            [`.${WebC__API_Markdown_To_Html.class__markdown_section}`    ] : { 'background-color' : '#F0F0FF'           ,
                                                                               'margin'           : '10px'              ,
                                                                               'padding'          : '10px'              },
            [`.${WebC__API_Markdown_To_Html.class__markdown_title}`      ] : { 'font-size'        : '24px'              ,
                                                                               'font-weight'      : 'bold'              ,
                                                                               'margin-bottom'    : '8px'               },
            [`.${WebC__API_Markdown_To_Html.class__markdown_sub_title}`  ] : { 'font-size'        : '20px'              ,
                                                                               'font-weight'     : 'normal'             ,
                                                                               'color'           : '#555'               ,
                                                                               'margin-bottom'   : '6px'                },
            [`.${WebC__API_Markdown_To_Html.class__markdown_description}`] : { 'font-size'        : '16px'              ,
                                                                               'font-style'      : 'italic'             ,
                                                                               'color'           : '#666'               ,
                                                                               'margin-bottom'   : '12px'               },
            [`.${WebC__API_Markdown_To_Html.class__markdown_error}`      ] : { 'font-size'        : '16px'              ,
                                                                               'font-style'      : 'italic'             ,
                                                                               'color'           : 'red'                },
            [`.${WebC__API_Markdown_To_Html.class__markdown_html}`]        : { }};
    }

    async load_html_content_and_metadata() {
        const method           = 'get'
        const target_url       = WebC__API_Markdown_To_Html.url__api_markdown_file_to_html_and_metadata + this.content_path
        const html_and_metadata = await this.api_invoke.invoke_api(target_url, method)
        this.markdown_html     = html_and_metadata.html
        this.markdown_metadata = html_and_metadata.metadata
    }

    async setup() {
        this.markdown_metadata                = null
        this.markdown_html                    = null
        this.api_invoke                       = new API__Invoke()
        this.api_invoke.mock_responses        = JSON.parse(this.getAttribute('mock_responses'))
        this.api_invoke.on_error_return_value = WebC__API_Markdown_To_Html.on_error_return_value
        await this.load_html_content_and_metadata()
    }
}

WebC__API_Markdown_To_Html.define()