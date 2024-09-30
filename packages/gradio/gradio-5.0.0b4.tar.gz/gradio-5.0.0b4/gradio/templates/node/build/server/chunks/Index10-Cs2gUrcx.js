import { c as create_ssr_component, a as createEventDispatcher, v as validate_component } from './ssr-Cz1f32Mr.js';
import { B as Block, S as Static } from './2-DpTvHskm.js';
import { U as UploadText } from './UploadText-ro6A0c4A.js';
import Gallery from './Gallery-CmLtn0hj.js';
import { B as BaseFileUpload } from './FileUpload-CJd2i2__.js';
import './index4-D_FyJKAV.js';
import './Upload2-CQQNjaMs.js';
import './BlockLabel-DhtaXLPo.js';
import './Empty-DpvP4MVd.js';
import './ShareButton-DPVoplEn.js';
import './Community-CFKRrddB.js';
import './Download-BYY54H3I.js';
import './Maximize-D0B3FhSj.js';
import './Image-DvwRtq0Q.js';
import './Play-Co7HyrpK.js';
import './IconButtonWrapper-BAn56FHd.js';
import './ModifyUpload-P2mCMyQR.js';
import './Undo-CbHQvbEr.js';
import './DownloadLink-4kzPen0P.js';
import './file-url-D-K40zdU.js';
import './Image2-CIpzhHTx.js';
import './Video2-CDNDBnbJ.js';
import './hls-CrxM9YLy.js';
import './File-B4mYSrEc.js';
import './Upload3-BYKJAdKj.js';

/* empty css                                       */
const Index = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let no_value;
  let { loading_status } = $$props;
  let { show_label } = $$props;
  let { label } = $$props;
  let { root } = $$props;
  let { elem_id = "" } = $$props;
  let { elem_classes = [] } = $$props;
  let { visible = true } = $$props;
  let { value = null } = $$props;
  let { file_types = ["image", "video"] } = $$props;
  let { container = true } = $$props;
  let { scale = null } = $$props;
  let { min_width = void 0 } = $$props;
  let { columns = [2] } = $$props;
  let { rows = void 0 } = $$props;
  let { height = "auto" } = $$props;
  let { preview } = $$props;
  let { allow_preview = true } = $$props;
  let { selected_index = null } = $$props;
  let { object_fit = "cover" } = $$props;
  let { show_share_button = false } = $$props;
  let { interactive } = $$props;
  let { show_download_button = false } = $$props;
  let { gradio } = $$props;
  let { show_fullscreen_button = true } = $$props;
  const dispatch = createEventDispatcher();
  if ($$props.loading_status === void 0 && $$bindings.loading_status && loading_status !== void 0)
    $$bindings.loading_status(loading_status);
  if ($$props.show_label === void 0 && $$bindings.show_label && show_label !== void 0)
    $$bindings.show_label(show_label);
  if ($$props.label === void 0 && $$bindings.label && label !== void 0)
    $$bindings.label(label);
  if ($$props.root === void 0 && $$bindings.root && root !== void 0)
    $$bindings.root(root);
  if ($$props.elem_id === void 0 && $$bindings.elem_id && elem_id !== void 0)
    $$bindings.elem_id(elem_id);
  if ($$props.elem_classes === void 0 && $$bindings.elem_classes && elem_classes !== void 0)
    $$bindings.elem_classes(elem_classes);
  if ($$props.visible === void 0 && $$bindings.visible && visible !== void 0)
    $$bindings.visible(visible);
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.file_types === void 0 && $$bindings.file_types && file_types !== void 0)
    $$bindings.file_types(file_types);
  if ($$props.container === void 0 && $$bindings.container && container !== void 0)
    $$bindings.container(container);
  if ($$props.scale === void 0 && $$bindings.scale && scale !== void 0)
    $$bindings.scale(scale);
  if ($$props.min_width === void 0 && $$bindings.min_width && min_width !== void 0)
    $$bindings.min_width(min_width);
  if ($$props.columns === void 0 && $$bindings.columns && columns !== void 0)
    $$bindings.columns(columns);
  if ($$props.rows === void 0 && $$bindings.rows && rows !== void 0)
    $$bindings.rows(rows);
  if ($$props.height === void 0 && $$bindings.height && height !== void 0)
    $$bindings.height(height);
  if ($$props.preview === void 0 && $$bindings.preview && preview !== void 0)
    $$bindings.preview(preview);
  if ($$props.allow_preview === void 0 && $$bindings.allow_preview && allow_preview !== void 0)
    $$bindings.allow_preview(allow_preview);
  if ($$props.selected_index === void 0 && $$bindings.selected_index && selected_index !== void 0)
    $$bindings.selected_index(selected_index);
  if ($$props.object_fit === void 0 && $$bindings.object_fit && object_fit !== void 0)
    $$bindings.object_fit(object_fit);
  if ($$props.show_share_button === void 0 && $$bindings.show_share_button && show_share_button !== void 0)
    $$bindings.show_share_button(show_share_button);
  if ($$props.interactive === void 0 && $$bindings.interactive && interactive !== void 0)
    $$bindings.interactive(interactive);
  if ($$props.show_download_button === void 0 && $$bindings.show_download_button && show_download_button !== void 0)
    $$bindings.show_download_button(show_download_button);
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  if ($$props.show_fullscreen_button === void 0 && $$bindings.show_fullscreen_button && show_fullscreen_button !== void 0)
    $$bindings.show_fullscreen_button(show_fullscreen_button);
  let $$settled;
  let $$rendered;
  let previous_head = $$result.head;
  do {
    $$settled = true;
    $$result.head = previous_head;
    no_value = value === null ? true : value.length === 0;
    {
      dispatch("prop_change", { selected_index });
    }
    $$rendered = `${validate_component(Block, "Block").$$render(
      $$result,
      {
        visible,
        variant: "solid",
        padding: false,
        elem_id,
        elem_classes,
        container,
        scale,
        min_width,
        allow_overflow: false,
        height: typeof height === "number" ? height : void 0
      },
      {},
      {
        default: () => {
          return `${validate_component(Static, "StatusTracker").$$render($$result, Object.assign({}, { autoscroll: gradio.autoscroll }, { i18n: gradio.i18n }, loading_status), {}, {})} ${interactive && no_value ? `${validate_component(BaseFileUpload, "BaseFileUpload").$$render(
            $$result,
            {
              value: null,
              root,
              label,
              max_file_size: gradio.max_file_size,
              file_count: "multiple",
              file_types,
              i18n: gradio.i18n,
              upload: (...args) => gradio.client.upload(...args),
              stream_handler: (...args) => gradio.client.stream(...args)
            },
            {},
            {
              default: () => {
                return `${validate_component(UploadText, "UploadText").$$render($$result, { i18n: gradio.i18n, type: "gallery" }, {}, {})}`;
              }
            }
          )}` : `${validate_component(Gallery, "Gallery").$$render(
            $$result,
            {
              label,
              show_label,
              columns,
              rows,
              height,
              preview,
              object_fit,
              interactive,
              allow_preview,
              show_share_button,
              show_download_button,
              i18n: gradio.i18n,
              _fetch: (...args) => gradio.client.fetch(...args),
              show_fullscreen_button,
              selected_index,
              value
            },
            {
              selected_index: ($$value) => {
                selected_index = $$value;
                $$settled = false;
              },
              value: ($$value) => {
                value = $$value;
                $$settled = false;
              }
            },
            {}
          )}`}`;
        }
      }
    )}`;
  } while (!$$settled);
  return $$rendered;
});

export { Gallery as BaseGallery, Index as default };
//# sourceMappingURL=Index10-Cs2gUrcx.js.map
