import { c as create_ssr_component, v as validate_component, b as add_attribute, e as escape } from './ssr-Cz1f32Mr.js';
import { B as Block, S as Static, h as BlockTitle } from './2-DpTvHskm.js';
import './index4-D_FyJKAV.js';

const css = {
  code: '.wrap.svelte-tnzk0w.svelte-tnzk0w{display:flex;flex-direction:column;width:100%}.head.svelte-tnzk0w.svelte-tnzk0w{margin-bottom:var(--size-2);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}.slider_input_container.svelte-tnzk0w.svelte-tnzk0w{display:flex;align-items:center;gap:var(--size-2)}input[type="range"].svelte-tnzk0w.svelte-tnzk0w{-webkit-appearance:none;appearance:none;width:100%;cursor:pointer;outline:none;border-radius:var(--radius-xl);min-width:var(--size-28)}input[type="range"].svelte-tnzk0w.svelte-tnzk0w::-webkit-slider-runnable-track{height:var(--size-2);background:var(--neutral-200);border-radius:var(--radius-xl)}input[type="range"].svelte-tnzk0w.svelte-tnzk0w::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;height:var(--size-4);width:var(--size-4);background-color:white;border-radius:50%;margin-top:-5px;box-shadow:0 0 0 1px rgba(247, 246, 246, 0.739),\n			1px 1px 4px rgba(0, 0, 0, 0.1)}input[type="range"].svelte-tnzk0w.svelte-tnzk0w::-webkit-slider-runnable-track{background:linear-gradient(\n			to right,\n			var(--color-accent) var(--range_progress),\n			var(--neutral-200) var(--range_progress)\n		)}input[type="range"].svelte-tnzk0w.svelte-tnzk0w::-moz-range-track{height:var(--size-2);background:var(--neutral-200);border-radius:var(--radius-xl)}input[type="range"].svelte-tnzk0w.svelte-tnzk0w::-moz-range-thumb{appearance:none;height:var(--size-4);width:var(--size-4);background-color:white;border-radius:50%;border:none;margin-top:calc(-1 * (var(--size-4) - var(--size-2)) / 2);box-shadow:0 0 0 1px rgba(247, 246, 246, 0.739),\n			1px 1px 4px rgba(0, 0, 0, 0.1)}input[type="range"].svelte-tnzk0w.svelte-tnzk0w::-moz-range-progress{height:var(--size-2);background-color:var(--color-accent);border-radius:var(--radius-xl)}input[type="number"].svelte-tnzk0w.svelte-tnzk0w{display:block;outline:none;border:1px solid var(--input-border-color);border-radius:var(--radius-sm);background:var(--input-background-fill);padding:var(--size-2) var(--size-3);height:var(--size-8);color:var(--body-text-color);font-size:var(--input-text-size);line-height:var(--line-sm);text-align:center;min-width:var(--size-16);transition:border-color 0.15s ease-in-out}input[type="number"].svelte-tnzk0w.svelte-tnzk0w:focus{box-shadow:none;border-width:2px}input.svelte-tnzk0w.svelte-tnzk0w:disabled,input[disabled].svelte-tnzk0w.svelte-tnzk0w{-webkit-text-fill-color:var(--body-text-color);opacity:1;cursor:not-allowed}input.svelte-tnzk0w.svelte-tnzk0w::placeholder{color:var(--input-placeholder-color)}input[type="range"][disabled].svelte-tnzk0w.svelte-tnzk0w{opacity:0.6}input[type="range"][disabled].svelte-tnzk0w.svelte-tnzk0w::-webkit-slider-thumb,input[type="range"][disabled].svelte-tnzk0w.svelte-tnzk0w::-moz-range-thumb,input[type="range"][disabled].svelte-tnzk0w.svelte-tnzk0w::-ms-thumb,input[type="range"][disabled].svelte-tnzk0w.svelte-tnzk0w::-webkit-slider-thumb:hover,input[type="range"][disabled].svelte-tnzk0w.svelte-tnzk0w::-moz-range-thumb:hover,input[type="range"][disabled].svelte-tnzk0w.svelte-tnzk0w::-moz-range-track:hover{background-color:var(--body-text-color-subdued);cursor:not-allowed}.min_value.svelte-tnzk0w.svelte-tnzk0w,.max_value.svelte-tnzk0w.svelte-tnzk0w{font-size:var(--text-sm);color:var(--body-text-color-subdued)}.min_value.svelte-tnzk0w.svelte-tnzk0w{margin-right:var(--size-0-5)}.max_value.svelte-tnzk0w.svelte-tnzk0w{margin-left:var(--size-0-5);margin-right:var(--size-0-5)}@media(max-width: 480px){.min_value.svelte-tnzk0w.svelte-tnzk0w,.max_value.svelte-tnzk0w.svelte-tnzk0w{display:none}}@media(max-width: 420px){.head.svelte-tnzk0w .tab-like-container.svelte-tnzk0w{margin-bottom:var(--size-4)}}.tab-like-container.svelte-tnzk0w.svelte-tnzk0w{display:flex;align-items:stretch;border:1px solid var(--input-border-color);border-radius:var(--radius-sm);overflow:hidden;height:var(--size-6)}input[type="number"].svelte-tnzk0w.svelte-tnzk0w{border:none;border-radius:0;padding:var(--size-1) var(--size-2);height:100%;min-width:var(--size-14);font-size:var(--text-sm)}input[type="number"].svelte-tnzk0w.svelte-tnzk0w:focus{box-shadow:inset 0 0 0 1px var(--color-accent);border-radius:3px 0 0px 3px}.reset-button.svelte-tnzk0w.svelte-tnzk0w{display:flex;align-items:center;justify-content:center;background:none;border:none;border-left:1px solid var(--input-border-color);cursor:pointer;font-size:var(--text-sm);color:var(--body-text-color);padding:0 var(--size-2);min-width:var(--size-6);transition:background-color 0.15s ease-in-out}.reset-button.svelte-tnzk0w.svelte-tnzk0w:hover:not(:disabled){background-color:var(--background-fill-secondary)}.reset-button.svelte-tnzk0w.svelte-tnzk0w:disabled{opacity:0.5;cursor:not-allowed}',
  map: '{"version":3,"file":"Index.svelte","sources":["Index.svelte"],"sourcesContent":["<script context=\\"module\\">\\n\\tlet _id = 0;\\n<\/script>\\n\\n<script lang=\\"ts\\">import { Block, BlockTitle } from \\"@gradio/atoms\\";\\nimport { StatusTracker } from \\"@gradio/statustracker\\";\\nimport { afterUpdate } from \\"svelte\\";\\nexport let gradio;\\nexport let elem_id = \\"\\";\\nexport let elem_classes = [];\\nexport let visible = true;\\nexport let value = 0;\\nlet initial_value = value;\\nexport let label = gradio.i18n(\\"slider.slider\\");\\nexport let info = void 0;\\nexport let container = true;\\nexport let scale = null;\\nexport let min_width = void 0;\\nexport let minimum;\\nexport let maximum = 100;\\nexport let step;\\nexport let show_label;\\nexport let interactive;\\nexport let loading_status;\\nexport let value_is_output = false;\\nlet range_input;\\nlet number_input;\\nconst id = `range_id_${_id++}`;\\nlet window_width;\\n$:\\n  minimum_value = minimum ?? 0;\\nfunction handle_change() {\\n  gradio.dispatch(\\"change\\");\\n  if (!value_is_output) {\\n    gradio.dispatch(\\"input\\");\\n  }\\n}\\nafterUpdate(() => {\\n  value_is_output = false;\\n  set_slider();\\n});\\nfunction handle_release(e) {\\n  gradio.dispatch(\\"release\\", value);\\n}\\nfunction clamp() {\\n  gradio.dispatch(\\"release\\", value);\\n  value = Math.min(Math.max(value, minimum), maximum);\\n}\\nfunction set_slider() {\\n  set_slider_range();\\n  range_input.addEventListener(\\"input\\", set_slider_range);\\n  number_input.addEventListener(\\"input\\", set_slider_range);\\n}\\nfunction set_slider_range() {\\n  const range = range_input;\\n  const min = Number(range.min) || 0;\\n  const max = Number(range.max) || 100;\\n  const val = Number(range.value) || 0;\\n  const percentage = (val - min) / (max - min) * 100;\\n  range.style.setProperty(\\"--range_progress\\", `${percentage}%`);\\n}\\n$:\\n  disabled = !interactive;\\n$:\\n  value, handle_change();\\nfunction handle_resize() {\\n  window_width = window.innerWidth;\\n}\\nfunction reset_value() {\\n  value = initial_value;\\n  set_slider_range();\\n  gradio.dispatch(\\"change\\");\\n  gradio.dispatch(\\"release\\", value);\\n}\\n<\/script>\\n\\n<svelte:window on:resize={handle_resize} />\\n\\n<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>\\n\\t<StatusTracker\\n\\t\\tautoscroll={gradio.autoscroll}\\n\\t\\ti18n={gradio.i18n}\\n\\t\\t{...loading_status}\\n\\t\\ton:clear_status={() => gradio.dispatch(\\"clear_status\\", loading_status)}\\n\\t/>\\n\\n\\t<div class=\\"wrap\\">\\n\\t\\t<div class=\\"head\\">\\n\\t\\t\\t<label for={id}>\\n\\t\\t\\t\\t<BlockTitle {show_label} {info}>{label}</BlockTitle>\\n\\t\\t\\t</label>\\n\\t\\t\\t<div class=\\"tab-like-container\\">\\n\\t\\t\\t\\t<input\\n\\t\\t\\t\\t\\taria-label={`number input for ${label}`}\\n\\t\\t\\t\\t\\tdata-testid=\\"number-input\\"\\n\\t\\t\\t\\t\\ttype=\\"number\\"\\n\\t\\t\\t\\t\\tbind:value\\n\\t\\t\\t\\t\\tbind:this={number_input}\\n\\t\\t\\t\\t\\tmin={minimum}\\n\\t\\t\\t\\t\\tmax={maximum}\\n\\t\\t\\t\\t\\ton:blur={clamp}\\n\\t\\t\\t\\t\\t{step}\\n\\t\\t\\t\\t\\t{disabled}\\n\\t\\t\\t\\t\\ton:pointerup={handle_release}\\n\\t\\t\\t\\t/>\\n\\t\\t\\t\\t<button\\n\\t\\t\\t\\t\\tclass=\\"reset-button\\"\\n\\t\\t\\t\\t\\ton:click={reset_value}\\n\\t\\t\\t\\t\\t{disabled}\\n\\t\\t\\t\\t\\taria-label=\\"Reset to default value\\"\\n\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t↺\\n\\t\\t\\t\\t</button>\\n\\t\\t\\t</div>\\n\\t\\t</div>\\n\\n\\t\\t<div class=\\"slider_input_container\\">\\n\\t\\t\\t<span class=\\"min_value\\">{minimum_value}</span>\\n\\t\\t\\t<input\\n\\t\\t\\t\\ttype=\\"range\\"\\n\\t\\t\\t\\t{id}\\n\\t\\t\\t\\tname=\\"cowbell\\"\\n\\t\\t\\t\\tbind:value\\n\\t\\t\\t\\tbind:this={range_input}\\n\\t\\t\\t\\tmin={minimum}\\n\\t\\t\\t\\tmax={maximum}\\n\\t\\t\\t\\t{step}\\n\\t\\t\\t\\t{disabled}\\n\\t\\t\\t\\ton:pointerup={handle_release}\\n\\t\\t\\t\\taria-label={`range slider for ${label}`}\\n\\t\\t\\t/>\\n\\t\\t\\t<span class=\\"max_value\\">{maximum}</span>\\n\\t\\t</div>\\n\\t</div>\\n</Block>\\n\\n<style>\\n\\t.wrap {\\n\\t\\tdisplay: flex;\\n\\t\\tflex-direction: column;\\n\\t\\twidth: 100%;\\n\\t}\\n\\n\\t.head {\\n\\t\\tmargin-bottom: var(--size-2);\\n\\t\\tdisplay: flex;\\n\\t\\tjustify-content: space-between;\\n\\t\\talign-items: center;\\n\\t\\tflex-wrap: wrap;\\n\\t}\\n\\n\\t.slider_input_container {\\n\\t\\tdisplay: flex;\\n\\t\\talign-items: center;\\n\\t\\tgap: var(--size-2);\\n\\t}\\n\\n\\tinput[type=\\"range\\"] {\\n\\t\\t-webkit-appearance: none;\\n\\t\\tappearance: none;\\n\\t\\twidth: 100%;\\n\\t\\tcursor: pointer;\\n\\t\\toutline: none;\\n\\t\\tborder-radius: var(--radius-xl);\\n\\t\\tmin-width: var(--size-28);\\n\\t}\\n\\n\\t/* webkit track */\\n\\tinput[type=\\"range\\"]::-webkit-slider-runnable-track {\\n\\t\\theight: var(--size-2);\\n\\t\\tbackground: var(--neutral-200);\\n\\t\\tborder-radius: var(--radius-xl);\\n\\t}\\n\\n\\t/* webkit thumb */\\n\\tinput[type=\\"range\\"]::-webkit-slider-thumb {\\n\\t\\t-webkit-appearance: none;\\n\\t\\tappearance: none;\\n\\t\\theight: var(--size-4);\\n\\t\\twidth: var(--size-4);\\n\\t\\tbackground-color: white;\\n\\t\\tborder-radius: 50%;\\n\\t\\tmargin-top: -5px;\\n\\t\\tbox-shadow:\\n\\t\\t\\t0 0 0 1px rgba(247, 246, 246, 0.739),\\n\\t\\t\\t1px 1px 4px rgba(0, 0, 0, 0.1);\\n\\t}\\n\\n\\tinput[type=\\"range\\"]::-webkit-slider-runnable-track {\\n\\t\\tbackground: linear-gradient(\\n\\t\\t\\tto right,\\n\\t\\t\\tvar(--color-accent) var(--range_progress),\\n\\t\\t\\tvar(--neutral-200) var(--range_progress)\\n\\t\\t);\\n\\t}\\n\\n\\t/* firefox */\\n\\tinput[type=\\"range\\"]::-moz-range-track {\\n\\t\\theight: var(--size-2);\\n\\t\\tbackground: var(--neutral-200);\\n\\t\\tborder-radius: var(--radius-xl);\\n\\t}\\n\\n\\tinput[type=\\"range\\"]::-moz-range-thumb {\\n\\t\\tappearance: none;\\n\\t\\theight: var(--size-4);\\n\\t\\twidth: var(--size-4);\\n\\t\\tbackground-color: white;\\n\\t\\tborder-radius: 50%;\\n\\t\\tborder: none;\\n\\t\\tmargin-top: calc(-1 * (var(--size-4) - var(--size-2)) / 2);\\n\\t\\tbox-shadow:\\n\\t\\t\\t0 0 0 1px rgba(247, 246, 246, 0.739),\\n\\t\\t\\t1px 1px 4px rgba(0, 0, 0, 0.1);\\n\\t}\\n\\n\\tinput[type=\\"range\\"]::-moz-range-progress {\\n\\t\\theight: var(--size-2);\\n\\t\\tbackground-color: var(--color-accent);\\n\\t\\tborder-radius: var(--radius-xl);\\n\\t}\\n\\n\\tinput[type=\\"number\\"] {\\n\\t\\tdisplay: block;\\n\\t\\toutline: none;\\n\\t\\tborder: 1px solid var(--input-border-color);\\n\\t\\tborder-radius: var(--radius-sm);\\n\\t\\tbackground: var(--input-background-fill);\\n\\t\\tpadding: var(--size-2) var(--size-3);\\n\\t\\theight: var(--size-8);\\n\\t\\tcolor: var(--body-text-color);\\n\\t\\tfont-size: var(--input-text-size);\\n\\t\\tline-height: var(--line-sm);\\n\\t\\ttext-align: center;\\n\\t\\tmin-width: var(--size-16);\\n\\t\\ttransition: border-color 0.15s ease-in-out;\\n\\t}\\n\\n\\tinput[type=\\"number\\"]:focus {\\n\\t\\tbox-shadow: none;\\n\\t\\tborder-width: 2px;\\n\\t}\\n\\n\\tinput:disabled,\\n\\tinput[disabled] {\\n\\t\\t-webkit-text-fill-color: var(--body-text-color);\\n\\t\\topacity: 1;\\n\\t\\tcursor: not-allowed;\\n\\t}\\n\\n\\tinput::placeholder {\\n\\t\\tcolor: var(--input-placeholder-color);\\n\\t}\\n\\n\\tinput[type=\\"range\\"][disabled] {\\n\\t\\topacity: 0.6;\\n\\t}\\n\\n\\tinput[type=\\"range\\"][disabled]::-webkit-slider-thumb,\\n\\tinput[type=\\"range\\"][disabled]::-moz-range-thumb,\\n\\tinput[type=\\"range\\"][disabled]::-ms-thumb,\\n\\tinput[type=\\"range\\"][disabled]::-webkit-slider-thumb:hover,\\n\\tinput[type=\\"range\\"][disabled]::-moz-range-thumb:hover,\\n\\tinput[type=\\"range\\"][disabled]::-moz-range-track:hover {\\n\\t\\tbackground-color: var(--body-text-color-subdued);\\n\\t\\tcursor: not-allowed;\\n\\t}\\n\\n\\t.min_value,\\n\\t.max_value {\\n\\t\\tfont-size: var(--text-sm);\\n\\t\\tcolor: var(--body-text-color-subdued);\\n\\t}\\n\\n\\t.min_value {\\n\\t\\tmargin-right: var(--size-0-5);\\n\\t}\\n\\n\\t.max_value {\\n\\t\\tmargin-left: var(--size-0-5);\\n\\t\\tmargin-right: var(--size-0-5);\\n\\t}\\n\\n\\t@media (max-width: 480px) {\\n\\t\\t.min_value,\\n\\t\\t.max_value {\\n\\t\\t\\tdisplay: none;\\n\\t\\t}\\n\\t}\\n\\n\\t@media (max-width: 420px) {\\n\\t\\t.head .tab-like-container {\\n\\t\\t\\tmargin-bottom: var(--size-4);\\n\\t\\t}\\n\\t}\\n\\n\\t.tab-like-container {\\n\\t\\tdisplay: flex;\\n\\t\\talign-items: stretch;\\n\\t\\tborder: 1px solid var(--input-border-color);\\n\\t\\tborder-radius: var(--radius-sm);\\n\\t\\toverflow: hidden;\\n\\t\\theight: var(--size-6);\\n\\t}\\n\\n\\tinput[type=\\"number\\"] {\\n\\t\\tborder: none;\\n\\t\\tborder-radius: 0;\\n\\t\\tpadding: var(--size-1) var(--size-2);\\n\\t\\theight: 100%;\\n\\t\\tmin-width: var(--size-14);\\n\\t\\tfont-size: var(--text-sm);\\n\\t}\\n\\n\\tinput[type=\\"number\\"]:focus {\\n\\t\\tbox-shadow: inset 0 0 0 1px var(--color-accent);\\n\\t\\tborder-radius: 3px 0 0px 3px;\\n\\t}\\n\\n\\t.reset-button {\\n\\t\\tdisplay: flex;\\n\\t\\talign-items: center;\\n\\t\\tjustify-content: center;\\n\\t\\tbackground: none;\\n\\t\\tborder: none;\\n\\t\\tborder-left: 1px solid var(--input-border-color);\\n\\t\\tcursor: pointer;\\n\\t\\tfont-size: var(--text-sm);\\n\\t\\tcolor: var(--body-text-color);\\n\\t\\tpadding: 0 var(--size-2);\\n\\t\\tmin-width: var(--size-6);\\n\\t\\ttransition: background-color 0.15s ease-in-out;\\n\\t}\\n\\n\\t.reset-button:hover:not(:disabled) {\\n\\t\\tbackground-color: var(--background-fill-secondary);\\n\\t}\\n\\n\\t.reset-button:disabled {\\n\\t\\topacity: 0.5;\\n\\t\\tcursor: not-allowed;\\n\\t}\\n</style>\\n"],"names":[],"mappings":"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"}'
};
let _id = 0;
const Index = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let minimum_value;
  let disabled;
  let { gradio } = $$props;
  let { elem_id = "" } = $$props;
  let { elem_classes = [] } = $$props;
  let { visible = true } = $$props;
  let { value = 0 } = $$props;
  let { label = gradio.i18n("slider.slider") } = $$props;
  let { info = void 0 } = $$props;
  let { container = true } = $$props;
  let { scale = null } = $$props;
  let { min_width = void 0 } = $$props;
  let { minimum } = $$props;
  let { maximum = 100 } = $$props;
  let { step } = $$props;
  let { show_label } = $$props;
  let { interactive } = $$props;
  let { loading_status } = $$props;
  let { value_is_output = false } = $$props;
  let range_input;
  let number_input;
  const id = `range_id_${_id++}`;
  function handle_change() {
    gradio.dispatch("change");
    if (!value_is_output) {
      gradio.dispatch("input");
    }
  }
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  if ($$props.elem_id === void 0 && $$bindings.elem_id && elem_id !== void 0)
    $$bindings.elem_id(elem_id);
  if ($$props.elem_classes === void 0 && $$bindings.elem_classes && elem_classes !== void 0)
    $$bindings.elem_classes(elem_classes);
  if ($$props.visible === void 0 && $$bindings.visible && visible !== void 0)
    $$bindings.visible(visible);
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.label === void 0 && $$bindings.label && label !== void 0)
    $$bindings.label(label);
  if ($$props.info === void 0 && $$bindings.info && info !== void 0)
    $$bindings.info(info);
  if ($$props.container === void 0 && $$bindings.container && container !== void 0)
    $$bindings.container(container);
  if ($$props.scale === void 0 && $$bindings.scale && scale !== void 0)
    $$bindings.scale(scale);
  if ($$props.min_width === void 0 && $$bindings.min_width && min_width !== void 0)
    $$bindings.min_width(min_width);
  if ($$props.minimum === void 0 && $$bindings.minimum && minimum !== void 0)
    $$bindings.minimum(minimum);
  if ($$props.maximum === void 0 && $$bindings.maximum && maximum !== void 0)
    $$bindings.maximum(maximum);
  if ($$props.step === void 0 && $$bindings.step && step !== void 0)
    $$bindings.step(step);
  if ($$props.show_label === void 0 && $$bindings.show_label && show_label !== void 0)
    $$bindings.show_label(show_label);
  if ($$props.interactive === void 0 && $$bindings.interactive && interactive !== void 0)
    $$bindings.interactive(interactive);
  if ($$props.loading_status === void 0 && $$bindings.loading_status && loading_status !== void 0)
    $$bindings.loading_status(loading_status);
  if ($$props.value_is_output === void 0 && $$bindings.value_is_output && value_is_output !== void 0)
    $$bindings.value_is_output(value_is_output);
  $$result.css.add(css);
  minimum_value = minimum ?? 0;
  disabled = !interactive;
  {
    handle_change();
  }
  return ` ${validate_component(Block, "Block").$$render(
    $$result,
    {
      visible,
      elem_id,
      elem_classes,
      container,
      scale,
      min_width
    },
    {},
    {
      default: () => {
        return `${validate_component(Static, "StatusTracker").$$render($$result, Object.assign({}, { autoscroll: gradio.autoscroll }, { i18n: gradio.i18n }, loading_status), {}, {})} <div class="wrap svelte-tnzk0w"><div class="head svelte-tnzk0w"><label${add_attribute("for", id, 0)}>${validate_component(BlockTitle, "BlockTitle").$$render($$result, { show_label, info }, {}, {
          default: () => {
            return `${escape(label)}`;
          }
        })}</label> <div class="tab-like-container svelte-tnzk0w"><input${add_attribute("aria-label", `number input for ${label}`, 0)} data-testid="number-input" type="number"${add_attribute("min", minimum, 0)}${add_attribute("max", maximum, 0)}${add_attribute("step", step, 0)} ${disabled ? "disabled" : ""} class="svelte-tnzk0w"${add_attribute("value", value, 0)}${add_attribute("this", number_input, 0)}> <button class="reset-button svelte-tnzk0w" ${disabled ? "disabled" : ""} aria-label="Reset to default value">↺</button></div></div> <div class="slider_input_container svelte-tnzk0w"><span class="min_value svelte-tnzk0w">${escape(minimum_value)}</span> <input type="range"${add_attribute("id", id, 0)} name="cowbell"${add_attribute("min", minimum, 0)}${add_attribute("max", maximum, 0)}${add_attribute("step", step, 0)} ${disabled ? "disabled" : ""}${add_attribute("aria-label", `range slider for ${label}`, 0)} class="svelte-tnzk0w"${add_attribute("value", value, 0)}${add_attribute("this", range_input, 0)}> <span class="max_value svelte-tnzk0w">${escape(maximum)}</span></div></div>`;
      }
    }
  )}`;
});

export { Index as default };
//# sourceMappingURL=Index30-BiQpovXA.js.map
