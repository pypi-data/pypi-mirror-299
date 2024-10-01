import WebC__Target_Div             from "../../../js/utils/WebC__Target_Div.mjs";
import Web_Component                from "../../../js/core/Web_Component.mjs";
import API__Invoke                  from "../../../js/data/API__Invoke.mjs";
import WebC__Markdown__Side_Menu   from "../../../js/elements/markdown/WebC__Markdown__Side_Menu.mjs";
import WebC__API_Markdown_To_Html from "../../../js/elements/api/WebC__API_Markdown_To_Html.mjs";
import Load_Libraries__CSS from "../../../js/utils/Load_Libraries__CSS.mjs";



QUnit.module('WebC__Markdown__Side_Menu', function(hooks) {
    let target_div
    let webc__markdown_side_menu
    let mock_responses
    let api_path
    let content_path

    hooks.beforeEach(async (assert) =>{
        content_path             = 'en/web-pages/demos/index.md'
        target_div               = WebC__Target_Div.add_to_body()
        mock_responses           = JSON.stringify(api_mock_data())
        let attributes           = { content_path:content_path, mock_responses: mock_responses, api_path: api_path }
        webc__markdown_side_menu = await target_div.append_child(WebC__Markdown__Side_Menu, attributes)
    })

    hooks.afterEach(() => {
        webc__markdown_side_menu.remove()
        target_div              .remove()
    })

    function api_mock_data() {
        const url__api_markdown_file_to_html_and_metadata  = WebC__Markdown__Side_Menu.url__api_markdown_file_to_html_and_metadata + content_path
        const url__css__material_design_icons              = Load_Libraries__CSS.url__css__material_design_icons
        const data__api_markdown_file_to_html_and_metadata = {'html': expected_raw_html, metadata: expected_metadata}
        return { [url__api_markdown_file_to_html_and_metadata]: data__api_markdown_file_to_html_and_metadata ,
                 [url__css__material_design_icons]            : '.simple {css : "code"} ' }
    }

    QUnit.test('.constructor', (assert) => {
        assert.deepEqual(target_div.constructor.name                       , 'WebC__Target_Div'                            )
        assert.deepEqual(WebC__Markdown__Side_Menu.name                    , 'WebC__Markdown__Side_Menu'                   )
        assert.deepEqual(webc__markdown_side_menu.content_path             , content_path                                  )
        assert.deepEqual(webc__markdown_side_menu.getAttributeNames()      , ['content_path', 'mock_responses', 'api_path'])
        assert.deepEqual(webc__markdown_side_menu.api_invoke.mock_responses, JSON.parse(mock_responses)                    )

        assert.ok       (WebC__Markdown__Side_Menu.prototype     instanceof Web_Component              )
        assert.ok       (webc__markdown_side_menu                instanceof WebC__API_Markdown_To_Html )
        assert.ok       (webc__markdown_side_menu                instanceof Web_Component              )
        assert.ok       (webc__markdown_side_menu                instanceof HTMLElement                )
        assert.ok       (webc__markdown_side_menu.api_invoke     instanceof API__Invoke                )
        assert.ok       (webc__markdown_side_menu.css_load_result.css_loaded)
    })

    QUnit.test('.build', (assert) => {
        assert.notDeepEqual(webc__markdown_side_menu.inner_html(), expected_html    )
    })

    const expected_raw_html = `<h2>Side menu</h2>\\n<p>this is the side menu</p>\\n<li class=\\"sidebar-item\\" data-visibility=\\"all\\">\\n  <a class=\\"sidebar-link waves-effect waves-dark sidebar-link\\" href=\\"home\\" aria-expanded=\\"false\\">\\n    <i class=\\"mdi me-2 mdi-home\\"></i>\\n    <span class=\\"hide-menu\\">Home</span>\\n  </a>\\n</li>\\n\\n<li class=\\"sidebar-item\\" data-visibility=\\"logged-in\\">\\n  <a class=\\"sidebar-link waves-effect waves-dark sidebar-link\\" href=\\"user/profile\\" aria-expanded=\\"false\\">\\n    <i class=\\"mdi me-2 mdi-account-check\\"></i>\\n    <span class=\\"hide-menu\\">Profile</span>\\n  </a>\\n</li>\\n\\n<li class=\\"sidebar-item\\" data-visibility=\\"logged-out\\">\\n  <a class=\\"sidebar-link waves-effect waves-dark sidebar-link\\" href=\\"login\\" aria-expanded=\\"false\\">\\n    <i class=\\"mdi me-2 mdi-login\\"></i>\\n    <span class=\\"hide-menu\\">Login</span>\\n  </a>\\n</li>\\n\\n<li class=\\"sidebar-item\\" data-visibility=\\"group:CBR-Team\\">\\n  <a class=\\"sidebar-link waves-effect waves-dark sidebar-link\\" href=\\"dev\\" aria-expanded=\\"false\\">\\n    <i class=\\"mdi me-2 mdi-developer-board\\"></i>\\n    <span class=\\"hide-menu\\">Dev</span>\\n  </a>\\n</li>\\n\\n<!-- Additional menu items... -->`
    const expected_metadata = {'title': 'the menu title'}
    const expected_html = `\
<div class="side_menu_section">
    <div class="side_menu_item">
    </div>
</div>
`

})