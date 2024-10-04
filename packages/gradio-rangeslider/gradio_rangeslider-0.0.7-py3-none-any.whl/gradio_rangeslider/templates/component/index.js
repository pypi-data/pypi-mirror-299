const {
  SvelteComponent: Xt,
  assign: Yt,
  create_slot: Gt,
  detach: Ht,
  element: Kt,
  get_all_dirty_from_scope: Qt,
  get_slot_changes: Ut,
  get_spread_update: Wt,
  init: xt,
  insert: $t,
  safe_not_equal: el,
  set_dynamic_element_data: lt,
  set_style: X,
  toggle_class: ee,
  transition_in: Mt,
  transition_out: Vt,
  update_slot_base: tl
} = window.__gradio__svelte__internal;
function ll(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), s = Gt(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let a = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], u = {};
  for (let f = 0; f < a.length; f += 1)
    u = Yt(u, a[f]);
  return {
    c() {
      e = Kt(
        /*tag*/
        l[14]
      ), s && s.c(), lt(
        /*tag*/
        l[14]
      )(e, u), ee(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), ee(
        e,
        "padded",
        /*padding*/
        l[6]
      ), ee(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), ee(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), ee(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), X(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), X(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), X(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), X(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), X(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), X(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), X(e, "border-width", "var(--block-border-width)");
    },
    m(f, o) {
      $t(f, e, o), s && s.m(e, null), n = !0;
    },
    p(f, o) {
      s && s.p && (!n || o & /*$$scope*/
      131072) && tl(
        s,
        i,
        f,
        /*$$scope*/
        f[17],
        n ? Ut(
          i,
          /*$$scope*/
          f[17],
          o,
          null
        ) : Qt(
          /*$$scope*/
          f[17]
        ),
        null
      ), lt(
        /*tag*/
        f[14]
      )(e, u = Wt(a, [
        (!n || o & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          f[7]
        ) },
        (!n || o & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          f[2]
        ) },
        (!n || o & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        f[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), ee(
        e,
        "hidden",
        /*visible*/
        f[10] === !1
      ), ee(
        e,
        "padded",
        /*padding*/
        f[6]
      ), ee(
        e,
        "border_focus",
        /*border_mode*/
        f[5] === "focus"
      ), ee(
        e,
        "border_contrast",
        /*border_mode*/
        f[5] === "contrast"
      ), ee(e, "hide-container", !/*explicit_call*/
      f[8] && !/*container*/
      f[9]), o & /*height*/
      1 && X(
        e,
        "height",
        /*get_dimension*/
        f[15](
          /*height*/
          f[0]
        )
      ), o & /*width*/
      2 && X(e, "width", typeof /*width*/
      f[1] == "number" ? `calc(min(${/*width*/
      f[1]}px, 100%))` : (
        /*get_dimension*/
        f[15](
          /*width*/
          f[1]
        )
      )), o & /*variant*/
      16 && X(
        e,
        "border-style",
        /*variant*/
        f[4]
      ), o & /*allow_overflow*/
      2048 && X(
        e,
        "overflow",
        /*allow_overflow*/
        f[11] ? "visible" : "hidden"
      ), o & /*scale*/
      4096 && X(
        e,
        "flex-grow",
        /*scale*/
        f[12]
      ), o & /*min_width*/
      8192 && X(e, "min-width", `calc(min(${/*min_width*/
      f[13]}px, 100%))`);
    },
    i(f) {
      n || (Mt(s, f), n = !0);
    },
    o(f) {
      Vt(s, f), n = !1;
    },
    d(f) {
      f && Ht(e), s && s.d(f);
    }
  };
}
function nl(l) {
  let e, t = (
    /*tag*/
    l[14] && ll(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (Mt(t, n), e = !0);
    },
    o(n) {
      Vt(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function il(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: s = void 0 } = e, { width: a = void 0 } = e, { elem_id: u = "" } = e, { elem_classes: f = [] } = e, { variant: o = "solid" } = e, { border_mode: r = "base" } = e, { padding: c = !0 } = e, { type: b = "normal" } = e, { test_id: g = void 0 } = e, { explicit_call: v = !1 } = e, { container: M = !0 } = e, { visible: C = !0 } = e, { allow_overflow: I = !0 } = e, { scale: m = null } = e, { min_width: d = 0 } = e, q = b === "fieldset" ? "fieldset" : "div";
  const A = (p) => {
    if (p !== void 0) {
      if (typeof p == "number")
        return p + "px";
      if (typeof p == "string")
        return p;
    }
  };
  return l.$$set = (p) => {
    "height" in p && t(0, s = p.height), "width" in p && t(1, a = p.width), "elem_id" in p && t(2, u = p.elem_id), "elem_classes" in p && t(3, f = p.elem_classes), "variant" in p && t(4, o = p.variant), "border_mode" in p && t(5, r = p.border_mode), "padding" in p && t(6, c = p.padding), "type" in p && t(16, b = p.type), "test_id" in p && t(7, g = p.test_id), "explicit_call" in p && t(8, v = p.explicit_call), "container" in p && t(9, M = p.container), "visible" in p && t(10, C = p.visible), "allow_overflow" in p && t(11, I = p.allow_overflow), "scale" in p && t(12, m = p.scale), "min_width" in p && t(13, d = p.min_width), "$$scope" in p && t(17, i = p.$$scope);
  }, [
    s,
    a,
    u,
    f,
    o,
    r,
    c,
    g,
    v,
    M,
    C,
    I,
    m,
    d,
    q,
    A,
    b,
    i,
    n
  ];
}
class fl extends Xt {
  constructor(e) {
    super(), xt(this, e, il, nl, el, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: sl,
  attr: ol,
  create_slot: al,
  detach: ul,
  element: rl,
  get_all_dirty_from_scope: _l,
  get_slot_changes: cl,
  init: dl,
  insert: ml,
  safe_not_equal: bl,
  transition_in: gl,
  transition_out: hl,
  update_slot_base: wl
} = window.__gradio__svelte__internal;
function pl(l) {
  let e, t;
  const n = (
    /*#slots*/
    l[1].default
  ), i = al(
    n,
    l,
    /*$$scope*/
    l[0],
    null
  );
  return {
    c() {
      e = rl("div"), i && i.c(), ol(e, "class", "svelte-1hnfib2");
    },
    m(s, a) {
      ml(s, e, a), i && i.m(e, null), t = !0;
    },
    p(s, [a]) {
      i && i.p && (!t || a & /*$$scope*/
      1) && wl(
        i,
        n,
        s,
        /*$$scope*/
        s[0],
        t ? cl(
          n,
          /*$$scope*/
          s[0],
          a,
          null
        ) : _l(
          /*$$scope*/
          s[0]
        ),
        null
      );
    },
    i(s) {
      t || (gl(i, s), t = !0);
    },
    o(s) {
      hl(i, s), t = !1;
    },
    d(s) {
      s && ul(e), i && i.d(s);
    }
  };
}
function kl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  return l.$$set = (s) => {
    "$$scope" in s && t(0, i = s.$$scope);
  }, [i, n];
}
class vl extends sl {
  constructor(e) {
    super(), dl(this, e, kl, pl, bl, {});
  }
}
const {
  SvelteComponent: yl,
  attr: nt,
  check_outros: ql,
  create_component: Cl,
  create_slot: Fl,
  destroy_component: Ll,
  detach: Pe,
  element: Sl,
  empty: zl,
  get_all_dirty_from_scope: Ml,
  get_slot_changes: Vl,
  group_outros: Nl,
  init: Il,
  insert: Be,
  mount_component: Zl,
  safe_not_equal: jl,
  set_data: Pl,
  space: Bl,
  text: Al,
  toggle_class: we,
  transition_in: Se,
  transition_out: Ae,
  update_slot_base: Dl
} = window.__gradio__svelte__internal;
function it(l) {
  let e, t;
  return e = new vl({
    props: {
      $$slots: { default: [El] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Cl(e.$$.fragment);
    },
    m(n, i) {
      Zl(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i & /*$$scope, info*/
      10 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (Se(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ae(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ll(e, n);
    }
  };
}
function El(l) {
  let e;
  return {
    c() {
      e = Al(
        /*info*/
        l[1]
      );
    },
    m(t, n) {
      Be(t, e, n);
    },
    p(t, n) {
      n & /*info*/
      2 && Pl(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Pe(e);
    }
  };
}
function Tl(l) {
  let e, t, n, i;
  const s = (
    /*#slots*/
    l[2].default
  ), a = Fl(
    s,
    l,
    /*$$scope*/
    l[3],
    null
  );
  let u = (
    /*info*/
    l[1] && it(l)
  );
  return {
    c() {
      e = Sl("span"), a && a.c(), t = Bl(), u && u.c(), n = zl(), nt(e, "data-testid", "block-info"), nt(e, "class", "svelte-22c38v"), we(e, "sr-only", !/*show_label*/
      l[0]), we(e, "hide", !/*show_label*/
      l[0]), we(
        e,
        "has-info",
        /*info*/
        l[1] != null
      );
    },
    m(f, o) {
      Be(f, e, o), a && a.m(e, null), Be(f, t, o), u && u.m(f, o), Be(f, n, o), i = !0;
    },
    p(f, [o]) {
      a && a.p && (!i || o & /*$$scope*/
      8) && Dl(
        a,
        s,
        f,
        /*$$scope*/
        f[3],
        i ? Vl(
          s,
          /*$$scope*/
          f[3],
          o,
          null
        ) : Ml(
          /*$$scope*/
          f[3]
        ),
        null
      ), (!i || o & /*show_label*/
      1) && we(e, "sr-only", !/*show_label*/
      f[0]), (!i || o & /*show_label*/
      1) && we(e, "hide", !/*show_label*/
      f[0]), (!i || o & /*info*/
      2) && we(
        e,
        "has-info",
        /*info*/
        f[1] != null
      ), /*info*/
      f[1] ? u ? (u.p(f, o), o & /*info*/
      2 && Se(u, 1)) : (u = it(f), u.c(), Se(u, 1), u.m(n.parentNode, n)) : u && (Nl(), Ae(u, 1, 1, () => {
        u = null;
      }), ql());
    },
    i(f) {
      i || (Se(a, f), Se(u), i = !0);
    },
    o(f) {
      Ae(a, f), Ae(u), i = !1;
    },
    d(f) {
      f && (Pe(e), Pe(t), Pe(n)), a && a.d(f), u && u.d(f);
    }
  };
}
function Ol(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { show_label: s = !0 } = e, { info: a = void 0 } = e;
  return l.$$set = (u) => {
    "show_label" in u && t(0, s = u.show_label), "info" in u && t(1, a = u.info), "$$scope" in u && t(3, i = u.$$scope);
  }, [s, a, n, i];
}
class Jl extends yl {
  constructor(e) {
    super(), Il(this, e, Ol, Tl, jl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Rl,
  append: Ge,
  attr: oe,
  bubble: Xl,
  create_component: Yl,
  destroy_component: Gl,
  detach: Nt,
  element: He,
  init: Hl,
  insert: It,
  listen: Kl,
  mount_component: Ql,
  safe_not_equal: Ul,
  set_data: Wl,
  set_style: pe,
  space: xl,
  text: $l,
  toggle_class: J,
  transition_in: en,
  transition_out: tn
} = window.__gradio__svelte__internal;
function ft(l) {
  let e, t;
  return {
    c() {
      e = He("span"), t = $l(
        /*label*/
        l[1]
      ), oe(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      It(n, e, i), Ge(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && Wl(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && Nt(e);
    }
  };
}
function ln(l) {
  let e, t, n, i, s, a, u, f = (
    /*show_label*/
    l[2] && ft(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = He("button"), f && f.c(), t = xl(), n = He("div"), Yl(i.$$.fragment), oe(n, "class", "svelte-1lrphxw"), J(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), J(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), J(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], oe(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), oe(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), oe(
        e,
        "title",
        /*label*/
        l[1]
      ), oe(e, "class", "svelte-1lrphxw"), J(
        e,
        "pending",
        /*pending*/
        l[3]
      ), J(
        e,
        "padded",
        /*padded*/
        l[5]
      ), J(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), J(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), pe(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), pe(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), pe(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(o, r) {
      It(o, e, r), f && f.m(e, null), Ge(e, t), Ge(e, n), Ql(i, n, null), s = !0, a || (u = Kl(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), a = !0);
    },
    p(o, [r]) {
      /*show_label*/
      o[2] ? f ? f.p(o, r) : (f = ft(o), f.c(), f.m(e, t)) : f && (f.d(1), f = null), (!s || r & /*size*/
      16) && J(
        n,
        "small",
        /*size*/
        o[4] === "small"
      ), (!s || r & /*size*/
      16) && J(
        n,
        "large",
        /*size*/
        o[4] === "large"
      ), (!s || r & /*size*/
      16) && J(
        n,
        "medium",
        /*size*/
        o[4] === "medium"
      ), (!s || r & /*disabled*/
      128) && (e.disabled = /*disabled*/
      o[7]), (!s || r & /*label*/
      2) && oe(
        e,
        "aria-label",
        /*label*/
        o[1]
      ), (!s || r & /*hasPopup*/
      256) && oe(
        e,
        "aria-haspopup",
        /*hasPopup*/
        o[8]
      ), (!s || r & /*label*/
      2) && oe(
        e,
        "title",
        /*label*/
        o[1]
      ), (!s || r & /*pending*/
      8) && J(
        e,
        "pending",
        /*pending*/
        o[3]
      ), (!s || r & /*padded*/
      32) && J(
        e,
        "padded",
        /*padded*/
        o[5]
      ), (!s || r & /*highlight*/
      64) && J(
        e,
        "highlight",
        /*highlight*/
        o[6]
      ), (!s || r & /*transparent*/
      512) && J(
        e,
        "transparent",
        /*transparent*/
        o[9]
      ), r & /*disabled, _color*/
      4224 && pe(e, "color", !/*disabled*/
      o[7] && /*_color*/
      o[12] ? (
        /*_color*/
        o[12]
      ) : "var(--block-label-text-color)"), r & /*disabled, background*/
      1152 && pe(e, "--bg-color", /*disabled*/
      o[7] ? "auto" : (
        /*background*/
        o[10]
      )), r & /*offset*/
      2048 && pe(
        e,
        "margin-left",
        /*offset*/
        o[11] + "px"
      );
    },
    i(o) {
      s || (en(i.$$.fragment, o), s = !0);
    },
    o(o) {
      tn(i.$$.fragment, o), s = !1;
    },
    d(o) {
      o && Nt(e), f && f.d(), Gl(i), a = !1, u();
    }
  };
}
function nn(l, e, t) {
  let n, { Icon: i } = e, { label: s = "" } = e, { show_label: a = !1 } = e, { pending: u = !1 } = e, { size: f = "small" } = e, { padded: o = !0 } = e, { highlight: r = !1 } = e, { disabled: c = !1 } = e, { hasPopup: b = !1 } = e, { color: g = "var(--block-label-text-color)" } = e, { transparent: v = !1 } = e, { background: M = "var(--background-fill-primary)" } = e, { offset: C = 0 } = e;
  function I(m) {
    Xl.call(this, l, m);
  }
  return l.$$set = (m) => {
    "Icon" in m && t(0, i = m.Icon), "label" in m && t(1, s = m.label), "show_label" in m && t(2, a = m.show_label), "pending" in m && t(3, u = m.pending), "size" in m && t(4, f = m.size), "padded" in m && t(5, o = m.padded), "highlight" in m && t(6, r = m.highlight), "disabled" in m && t(7, c = m.disabled), "hasPopup" in m && t(8, b = m.hasPopup), "color" in m && t(13, g = m.color), "transparent" in m && t(9, v = m.transparent), "background" in m && t(10, M = m.background), "offset" in m && t(11, C = m.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = r ? "var(--color-accent)" : g);
  }, [
    i,
    s,
    a,
    u,
    f,
    o,
    r,
    c,
    b,
    v,
    M,
    C,
    n,
    g,
    I
  ];
}
class fn extends Rl {
  constructor(e) {
    super(), Hl(this, e, nn, ln, Ul, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: sn,
  append: Re,
  attr: K,
  detach: on,
  init: an,
  insert: un,
  noop: Xe,
  safe_not_equal: rn,
  set_style: te,
  svg_element: Ie
} = window.__gradio__svelte__internal;
function _n(l) {
  let e, t, n, i;
  return {
    c() {
      e = Ie("svg"), t = Ie("g"), n = Ie("path"), i = Ie("path"), K(n, "d", "M18,6L6.087,17.913"), te(n, "fill", "none"), te(n, "fill-rule", "nonzero"), te(n, "stroke-width", "2px"), K(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), K(i, "d", "M4.364,4.364L19.636,19.636"), te(i, "fill", "none"), te(i, "fill-rule", "nonzero"), te(i, "stroke-width", "2px"), K(e, "width", "100%"), K(e, "height", "100%"), K(e, "viewBox", "0 0 24 24"), K(e, "version", "1.1"), K(e, "xmlns", "http://www.w3.org/2000/svg"), K(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), K(e, "xml:space", "preserve"), K(e, "stroke", "currentColor"), te(e, "fill-rule", "evenodd"), te(e, "clip-rule", "evenodd"), te(e, "stroke-linecap", "round"), te(e, "stroke-linejoin", "round");
    },
    m(s, a) {
      un(s, e, a), Re(e, t), Re(t, n), Re(e, i);
    },
    p: Xe,
    i: Xe,
    o: Xe,
    d(s) {
      s && on(e);
    }
  };
}
class cn extends sn {
  constructor(e) {
    super(), an(this, e, null, _n, rn, {});
  }
}
const dn = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], st = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
dn.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: st[e][t],
      secondary: st[e][n]
    }
  }),
  {}
);
function ve(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function De() {
}
function mn(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const Zt = typeof window < "u";
let ot = Zt ? () => window.performance.now() : () => Date.now(), jt = Zt ? (l) => requestAnimationFrame(l) : De;
const qe = /* @__PURE__ */ new Set();
function Pt(l) {
  qe.forEach((e) => {
    e.c(l) || (qe.delete(e), e.f());
  }), qe.size !== 0 && jt(Pt);
}
function bn(l) {
  let e;
  return qe.size === 0 && jt(Pt), {
    promise: new Promise((t) => {
      qe.add(e = { c: l, f: t });
    }),
    abort() {
      qe.delete(e);
    }
  };
}
const ke = [];
function gn(l, e = De) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(u) {
    if (mn(l, u) && (l = u, t)) {
      const f = !ke.length;
      for (const o of n)
        o[1](), ke.push(o, l);
      if (f) {
        for (let o = 0; o < ke.length; o += 2)
          ke[o][0](ke[o + 1]);
        ke.length = 0;
      }
    }
  }
  function s(u) {
    i(u(l));
  }
  function a(u, f = De) {
    const o = [u, f];
    return n.add(o), n.size === 1 && (t = e(i, s) || De), u(l), () => {
      n.delete(o), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: s, subscribe: a };
}
function at(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function Ke(l, e, t, n) {
  if (typeof t == "number" || at(t)) {
    const i = n - t, s = (t - e) / (l.dt || 1 / 60), a = l.opts.stiffness * i, u = l.opts.damping * s, f = (a - u) * l.inv_mass, o = (s + f) * l.dt;
    return Math.abs(o) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, at(t) ? new Date(t.getTime() + o) : t + o);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, s) => Ke(l, e[s], t[s], n[s])
      );
    if (typeof t == "object") {
      const i = {};
      for (const s in t)
        i[s] = Ke(l, e[s], t[s], n[s]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function ut(l, e = {}) {
  const t = gn(l), { stiffness: n = 0.15, damping: i = 0.8, precision: s = 0.01 } = e;
  let a, u, f, o = l, r = l, c = 1, b = 0, g = !1;
  function v(C, I = {}) {
    r = C;
    const m = f = {};
    return l == null || I.hard || M.stiffness >= 1 && M.damping >= 1 ? (g = !0, a = ot(), o = C, t.set(l = r), Promise.resolve()) : (I.soft && (b = 1 / ((I.soft === !0 ? 0.5 : +I.soft) * 60), c = 0), u || (a = ot(), g = !1, u = bn((d) => {
      if (g)
        return g = !1, u = null, !1;
      c = Math.min(c + b, 1);
      const q = {
        inv_mass: c,
        opts: M,
        settled: !0,
        dt: (d - a) * 60 / 1e3
      }, A = Ke(q, o, l, r);
      return a = d, o = l, t.set(l = A), q.settled && (u = null), !q.settled;
    })), new Promise((d) => {
      u.promise.then(() => {
        m === f && d();
      });
    }));
  }
  const M = {
    set: v,
    update: (C, I) => v(C(r, l), I),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: s
  };
  return M;
}
const {
  SvelteComponent: hn,
  append: Q,
  attr: S,
  component_subscribe: rt,
  detach: wn,
  element: pn,
  init: kn,
  insert: vn,
  noop: _t,
  safe_not_equal: yn,
  set_style: Ze,
  svg_element: U,
  toggle_class: ct
} = window.__gradio__svelte__internal, { onMount: qn } = window.__gradio__svelte__internal;
function Cn(l) {
  let e, t, n, i, s, a, u, f, o, r, c, b;
  return {
    c() {
      e = pn("div"), t = U("svg"), n = U("g"), i = U("path"), s = U("path"), a = U("path"), u = U("path"), f = U("g"), o = U("path"), r = U("path"), c = U("path"), b = U("path"), S(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), S(i, "fill", "#FF7C00"), S(i, "fill-opacity", "0.4"), S(i, "class", "svelte-43sxxs"), S(s, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), S(s, "fill", "#FF7C00"), S(s, "class", "svelte-43sxxs"), S(a, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), S(a, "fill", "#FF7C00"), S(a, "fill-opacity", "0.4"), S(a, "class", "svelte-43sxxs"), S(u, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), S(u, "fill", "#FF7C00"), S(u, "class", "svelte-43sxxs"), Ze(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), S(o, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), S(o, "fill", "#FF7C00"), S(o, "fill-opacity", "0.4"), S(o, "class", "svelte-43sxxs"), S(r, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), S(r, "fill", "#FF7C00"), S(r, "class", "svelte-43sxxs"), S(c, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), S(c, "fill", "#FF7C00"), S(c, "fill-opacity", "0.4"), S(c, "class", "svelte-43sxxs"), S(b, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), S(b, "fill", "#FF7C00"), S(b, "class", "svelte-43sxxs"), Ze(f, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), S(t, "viewBox", "-1200 -1200 3000 3000"), S(t, "fill", "none"), S(t, "xmlns", "http://www.w3.org/2000/svg"), S(t, "class", "svelte-43sxxs"), S(e, "class", "svelte-43sxxs"), ct(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(g, v) {
      vn(g, e, v), Q(e, t), Q(t, n), Q(n, i), Q(n, s), Q(n, a), Q(n, u), Q(t, f), Q(f, o), Q(f, r), Q(f, c), Q(f, b);
    },
    p(g, [v]) {
      v & /*$top*/
      2 && Ze(n, "transform", "translate(" + /*$top*/
      g[1][0] + "px, " + /*$top*/
      g[1][1] + "px)"), v & /*$bottom*/
      4 && Ze(f, "transform", "translate(" + /*$bottom*/
      g[2][0] + "px, " + /*$bottom*/
      g[2][1] + "px)"), v & /*margin*/
      1 && ct(
        e,
        "margin",
        /*margin*/
        g[0]
      );
    },
    i: _t,
    o: _t,
    d(g) {
      g && wn(e);
    }
  };
}
function Fn(l, e, t) {
  let n, i;
  var s = this && this.__awaiter || function(g, v, M, C) {
    function I(m) {
      return m instanceof M ? m : new M(function(d) {
        d(m);
      });
    }
    return new (M || (M = Promise))(function(m, d) {
      function q(D) {
        try {
          p(C.next(D));
        } catch (B) {
          d(B);
        }
      }
      function A(D) {
        try {
          p(C.throw(D));
        } catch (B) {
          d(B);
        }
      }
      function p(D) {
        D.done ? m(D.value) : I(D.value).then(q, A);
      }
      p((C = C.apply(g, v || [])).next());
    });
  };
  let { margin: a = !0 } = e;
  const u = ut([0, 0]);
  rt(l, u, (g) => t(1, n = g));
  const f = ut([0, 0]);
  rt(l, f, (g) => t(2, i = g));
  let o;
  function r() {
    return s(this, void 0, void 0, function* () {
      yield Promise.all([u.set([125, 140]), f.set([-125, -140])]), yield Promise.all([u.set([-125, 140]), f.set([125, -140])]), yield Promise.all([u.set([-125, 0]), f.set([125, -0])]), yield Promise.all([u.set([125, 0]), f.set([-125, 0])]);
    });
  }
  function c() {
    return s(this, void 0, void 0, function* () {
      yield r(), o || c();
    });
  }
  function b() {
    return s(this, void 0, void 0, function* () {
      yield Promise.all([u.set([125, 0]), f.set([-125, 0])]), c();
    });
  }
  return qn(() => (b(), () => o = !0)), l.$$set = (g) => {
    "margin" in g && t(0, a = g.margin);
  }, [a, n, i, u, f];
}
class Ln extends hn {
  constructor(e) {
    super(), kn(this, e, Fn, Cn, yn, { margin: 0 });
  }
}
const {
  SvelteComponent: Sn,
  append: ce,
  attr: W,
  binding_callbacks: dt,
  check_outros: Bt,
  create_component: At,
  create_slot: zn,
  destroy_component: Dt,
  destroy_each: Et,
  detach: F,
  element: ne,
  empty: Ce,
  ensure_array_like: Te,
  get_all_dirty_from_scope: Mn,
  get_slot_changes: Vn,
  group_outros: Tt,
  init: Nn,
  insert: L,
  mount_component: Ot,
  noop: Qe,
  safe_not_equal: In,
  set_data: G,
  set_style: re,
  space: x,
  text: P,
  toggle_class: Y,
  transition_in: de,
  transition_out: me,
  update_slot_base: Zn
} = window.__gradio__svelte__internal, { tick: jn } = window.__gradio__svelte__internal, { onDestroy: Pn } = window.__gradio__svelte__internal, { createEventDispatcher: Bn } = window.__gradio__svelte__internal, An = (l) => ({}), mt = (l) => ({});
function bt(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function gt(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function Dn(l) {
  let e, t, n, i, s = (
    /*i18n*/
    l[1]("common.error") + ""
  ), a, u, f;
  t = new fn({
    props: {
      Icon: cn,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const o = (
    /*#slots*/
    l[30].error
  ), r = zn(
    o,
    l,
    /*$$scope*/
    l[29],
    mt
  );
  return {
    c() {
      e = ne("div"), At(t.$$.fragment), n = x(), i = ne("span"), a = P(s), u = x(), r && r.c(), W(e, "class", "clear-status svelte-1yk38uw"), W(i, "class", "error svelte-1yk38uw");
    },
    m(c, b) {
      L(c, e, b), Ot(t, e, null), L(c, n, b), L(c, i, b), ce(i, a), L(c, u, b), r && r.m(c, b), f = !0;
    },
    p(c, b) {
      const g = {};
      b[0] & /*i18n*/
      2 && (g.label = /*i18n*/
      c[1]("common.clear")), t.$set(g), (!f || b[0] & /*i18n*/
      2) && s !== (s = /*i18n*/
      c[1]("common.error") + "") && G(a, s), r && r.p && (!f || b[0] & /*$$scope*/
      536870912) && Zn(
        r,
        o,
        c,
        /*$$scope*/
        c[29],
        f ? Vn(
          o,
          /*$$scope*/
          c[29],
          b,
          An
        ) : Mn(
          /*$$scope*/
          c[29]
        ),
        mt
      );
    },
    i(c) {
      f || (de(t.$$.fragment, c), de(r, c), f = !0);
    },
    o(c) {
      me(t.$$.fragment, c), me(r, c), f = !1;
    },
    d(c) {
      c && (F(e), F(n), F(i), F(u)), Dt(t), r && r.d(c);
    }
  };
}
function En(l) {
  let e, t, n, i, s, a, u, f, o, r = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && ht(l)
  );
  function c(d, q) {
    if (
      /*progress*/
      d[7]
    )
      return Jn;
    if (
      /*queue_position*/
      d[2] !== null && /*queue_size*/
      d[3] !== void 0 && /*queue_position*/
      d[2] >= 0
    )
      return On;
    if (
      /*queue_position*/
      d[2] === 0
    )
      return Tn;
  }
  let b = c(l), g = b && b(l), v = (
    /*timer*/
    l[5] && kt(l)
  );
  const M = [Gn, Yn], C = [];
  function I(d, q) {
    return (
      /*last_progress_level*/
      d[15] != null ? 0 : (
        /*show_progress*/
        d[6] === "full" ? 1 : -1
      )
    );
  }
  ~(s = I(l)) && (a = C[s] = M[s](l));
  let m = !/*timer*/
  l[5] && St(l);
  return {
    c() {
      r && r.c(), e = x(), t = ne("div"), g && g.c(), n = x(), v && v.c(), i = x(), a && a.c(), u = x(), m && m.c(), f = Ce(), W(t, "class", "progress-text svelte-1yk38uw"), Y(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), Y(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(d, q) {
      r && r.m(d, q), L(d, e, q), L(d, t, q), g && g.m(t, null), ce(t, n), v && v.m(t, null), L(d, i, q), ~s && C[s].m(d, q), L(d, u, q), m && m.m(d, q), L(d, f, q), o = !0;
    },
    p(d, q) {
      /*variant*/
      d[8] === "default" && /*show_eta_bar*/
      d[18] && /*show_progress*/
      d[6] === "full" ? r ? r.p(d, q) : (r = ht(d), r.c(), r.m(e.parentNode, e)) : r && (r.d(1), r = null), b === (b = c(d)) && g ? g.p(d, q) : (g && g.d(1), g = b && b(d), g && (g.c(), g.m(t, n))), /*timer*/
      d[5] ? v ? v.p(d, q) : (v = kt(d), v.c(), v.m(t, null)) : v && (v.d(1), v = null), (!o || q[0] & /*variant*/
      256) && Y(
        t,
        "meta-text-center",
        /*variant*/
        d[8] === "center"
      ), (!o || q[0] & /*variant*/
      256) && Y(
        t,
        "meta-text",
        /*variant*/
        d[8] === "default"
      );
      let A = s;
      s = I(d), s === A ? ~s && C[s].p(d, q) : (a && (Tt(), me(C[A], 1, 1, () => {
        C[A] = null;
      }), Bt()), ~s ? (a = C[s], a ? a.p(d, q) : (a = C[s] = M[s](d), a.c()), de(a, 1), a.m(u.parentNode, u)) : a = null), /*timer*/
      d[5] ? m && (m.d(1), m = null) : m ? m.p(d, q) : (m = St(d), m.c(), m.m(f.parentNode, f));
    },
    i(d) {
      o || (de(a), o = !0);
    },
    o(d) {
      me(a), o = !1;
    },
    d(d) {
      d && (F(e), F(t), F(i), F(u), F(f)), r && r.d(d), g && g.d(), v && v.d(), ~s && C[s].d(d), m && m.d(d);
    }
  };
}
function ht(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = ne("div"), W(e, "class", "eta-bar svelte-1yk38uw"), re(e, "transform", t);
    },
    m(n, i) {
      L(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && re(e, "transform", t);
    },
    d(n) {
      n && F(e);
    }
  };
}
function Tn(l) {
  let e;
  return {
    c() {
      e = P("processing |");
    },
    m(t, n) {
      L(t, e, n);
    },
    p: Qe,
    d(t) {
      t && F(e);
    }
  };
}
function On(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, s, a;
  return {
    c() {
      e = P("queue: "), n = P(t), i = P("/"), s = P(
        /*queue_size*/
        l[3]
      ), a = P(" |");
    },
    m(u, f) {
      L(u, e, f), L(u, n, f), L(u, i, f), L(u, s, f), L(u, a, f);
    },
    p(u, f) {
      f[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      u[2] + 1 + "") && G(n, t), f[0] & /*queue_size*/
      8 && G(
        s,
        /*queue_size*/
        u[3]
      );
    },
    d(u) {
      u && (F(e), F(n), F(i), F(s), F(a));
    }
  };
}
function Jn(l) {
  let e, t = Te(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = pt(gt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Ce();
    },
    m(i, s) {
      for (let a = 0; a < n.length; a += 1)
        n[a] && n[a].m(i, s);
      L(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress*/
      128) {
        t = Te(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const u = gt(i, t, a);
          n[a] ? n[a].p(u, s) : (n[a] = pt(u), n[a].c(), n[a].m(e.parentNode, e));
        }
        for (; a < n.length; a += 1)
          n[a].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && F(e), Et(n, i);
    }
  };
}
function wt(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, s = " ", a;
  function u(r, c) {
    return (
      /*p*/
      r[41].length != null ? Xn : Rn
    );
  }
  let f = u(l), o = f(l);
  return {
    c() {
      o.c(), e = x(), n = P(t), i = P(" | "), a = P(s);
    },
    m(r, c) {
      o.m(r, c), L(r, e, c), L(r, n, c), L(r, i, c), L(r, a, c);
    },
    p(r, c) {
      f === (f = u(r)) && o ? o.p(r, c) : (o.d(1), o = f(r), o && (o.c(), o.m(e.parentNode, e))), c[0] & /*progress*/
      128 && t !== (t = /*p*/
      r[41].unit + "") && G(n, t);
    },
    d(r) {
      r && (F(e), F(n), F(i), F(a)), o.d(r);
    }
  };
}
function Rn(l) {
  let e = ve(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = P(e);
    },
    m(n, i) {
      L(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = ve(
        /*p*/
        n[41].index || 0
      ) + "") && G(t, e);
    },
    d(n) {
      n && F(t);
    }
  };
}
function Xn(l) {
  let e = ve(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = ve(
    /*p*/
    l[41].length
  ) + "", s;
  return {
    c() {
      t = P(e), n = P("/"), s = P(i);
    },
    m(a, u) {
      L(a, t, u), L(a, n, u), L(a, s, u);
    },
    p(a, u) {
      u[0] & /*progress*/
      128 && e !== (e = ve(
        /*p*/
        a[41].index || 0
      ) + "") && G(t, e), u[0] & /*progress*/
      128 && i !== (i = ve(
        /*p*/
        a[41].length
      ) + "") && G(s, i);
    },
    d(a) {
      a && (F(t), F(n), F(s));
    }
  };
}
function pt(l) {
  let e, t = (
    /*p*/
    l[41].index != null && wt(l)
  );
  return {
    c() {
      t && t.c(), e = Ce();
    },
    m(n, i) {
      t && t.m(n, i), L(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = wt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && F(e), t && t.d(n);
    }
  };
}
function kt(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = P(
        /*formatted_timer*/
        l[20]
      ), n = P(t), i = P("s");
    },
    m(s, a) {
      L(s, e, a), L(s, n, a), L(s, i, a);
    },
    p(s, a) {
      a[0] & /*formatted_timer*/
      1048576 && G(
        e,
        /*formatted_timer*/
        s[20]
      ), a[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      s[0] ? `/${/*formatted_eta*/
      s[19]}` : "") && G(n, t);
    },
    d(s) {
      s && (F(e), F(n), F(i));
    }
  };
}
function Yn(l) {
  let e, t;
  return e = new Ln({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      At(e.$$.fragment);
    },
    m(n, i) {
      Ot(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i[0] & /*variant*/
      256 && (s.margin = /*variant*/
      n[8] === "default"), e.$set(s);
    },
    i(n) {
      t || (de(e.$$.fragment, n), t = !0);
    },
    o(n) {
      me(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Dt(e, n);
    }
  };
}
function Gn(l) {
  let e, t, n, i, s, a = `${/*last_progress_level*/
  l[15] * 100}%`, u = (
    /*progress*/
    l[7] != null && vt(l)
  );
  return {
    c() {
      e = ne("div"), t = ne("div"), u && u.c(), n = x(), i = ne("div"), s = ne("div"), W(t, "class", "progress-level-inner svelte-1yk38uw"), W(s, "class", "progress-bar svelte-1yk38uw"), re(s, "width", a), W(i, "class", "progress-bar-wrap svelte-1yk38uw"), W(e, "class", "progress-level svelte-1yk38uw");
    },
    m(f, o) {
      L(f, e, o), ce(e, t), u && u.m(t, null), ce(e, n), ce(e, i), ce(i, s), l[31](s);
    },
    p(f, o) {
      /*progress*/
      f[7] != null ? u ? u.p(f, o) : (u = vt(f), u.c(), u.m(t, null)) : u && (u.d(1), u = null), o[0] & /*last_progress_level*/
      32768 && a !== (a = `${/*last_progress_level*/
      f[15] * 100}%`) && re(s, "width", a);
    },
    i: Qe,
    o: Qe,
    d(f) {
      f && F(e), u && u.d(), l[31](null);
    }
  };
}
function vt(l) {
  let e, t = Te(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Lt(bt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Ce();
    },
    m(i, s) {
      for (let a = 0; a < n.length; a += 1)
        n[a] && n[a].m(i, s);
      L(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress_level, progress*/
      16512) {
        t = Te(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const u = bt(i, t, a);
          n[a] ? n[a].p(u, s) : (n[a] = Lt(u), n[a].c(), n[a].m(e.parentNode, e));
        }
        for (; a < n.length; a += 1)
          n[a].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && F(e), Et(n, i);
    }
  };
}
function yt(l) {
  let e, t, n, i, s = (
    /*i*/
    l[43] !== 0 && Hn()
  ), a = (
    /*p*/
    l[41].desc != null && qt(l)
  ), u = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && Ct()
  ), f = (
    /*progress_level*/
    l[14] != null && Ft(l)
  );
  return {
    c() {
      s && s.c(), e = x(), a && a.c(), t = x(), u && u.c(), n = x(), f && f.c(), i = Ce();
    },
    m(o, r) {
      s && s.m(o, r), L(o, e, r), a && a.m(o, r), L(o, t, r), u && u.m(o, r), L(o, n, r), f && f.m(o, r), L(o, i, r);
    },
    p(o, r) {
      /*p*/
      o[41].desc != null ? a ? a.p(o, r) : (a = qt(o), a.c(), a.m(t.parentNode, t)) : a && (a.d(1), a = null), /*p*/
      o[41].desc != null && /*progress_level*/
      o[14] && /*progress_level*/
      o[14][
        /*i*/
        o[43]
      ] != null ? u || (u = Ct(), u.c(), u.m(n.parentNode, n)) : u && (u.d(1), u = null), /*progress_level*/
      o[14] != null ? f ? f.p(o, r) : (f = Ft(o), f.c(), f.m(i.parentNode, i)) : f && (f.d(1), f = null);
    },
    d(o) {
      o && (F(e), F(t), F(n), F(i)), s && s.d(o), a && a.d(o), u && u.d(o), f && f.d(o);
    }
  };
}
function Hn(l) {
  let e;
  return {
    c() {
      e = P(" /");
    },
    m(t, n) {
      L(t, e, n);
    },
    d(t) {
      t && F(e);
    }
  };
}
function qt(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = P(e);
    },
    m(n, i) {
      L(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && G(t, e);
    },
    d(n) {
      n && F(t);
    }
  };
}
function Ct(l) {
  let e;
  return {
    c() {
      e = P("-");
    },
    m(t, n) {
      L(t, e, n);
    },
    d(t) {
      t && F(e);
    }
  };
}
function Ft(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = P(e), n = P("%");
    },
    m(i, s) {
      L(i, t, s), L(i, n, s);
    },
    p(i, s) {
      s[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && G(t, e);
    },
    d(i) {
      i && (F(t), F(n));
    }
  };
}
function Lt(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && yt(l)
  );
  return {
    c() {
      t && t.c(), e = Ce();
    },
    m(n, i) {
      t && t.m(n, i), L(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = yt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && F(e), t && t.d(n);
    }
  };
}
function St(l) {
  let e, t;
  return {
    c() {
      e = ne("p"), t = P(
        /*loading_text*/
        l[9]
      ), W(e, "class", "loading svelte-1yk38uw");
    },
    m(n, i) {
      L(n, e, i), ce(e, t);
    },
    p(n, i) {
      i[0] & /*loading_text*/
      512 && G(
        t,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && F(e);
    }
  };
}
function Kn(l) {
  let e, t, n, i, s;
  const a = [En, Dn], u = [];
  function f(o, r) {
    return (
      /*status*/
      o[4] === "pending" ? 0 : (
        /*status*/
        o[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = f(l)) && (n = u[t] = a[t](l)), {
    c() {
      e = ne("div"), n && n.c(), W(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-1yk38uw"), Y(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), Y(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), Y(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), Y(
        e,
        "border",
        /*border*/
        l[12]
      ), re(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), re(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(o, r) {
      L(o, e, r), ~t && u[t].m(e, null), l[33](e), s = !0;
    },
    p(o, r) {
      let c = t;
      t = f(o), t === c ? ~t && u[t].p(o, r) : (n && (Tt(), me(u[c], 1, 1, () => {
        u[c] = null;
      }), Bt()), ~t ? (n = u[t], n ? n.p(o, r) : (n = u[t] = a[t](o), n.c()), de(n, 1), n.m(e, null)) : n = null), (!s || r[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      o[8] + " " + /*show_progress*/
      o[6] + " svelte-1yk38uw")) && W(e, "class", i), (!s || r[0] & /*variant, show_progress, status, show_progress*/
      336) && Y(e, "hide", !/*status*/
      o[4] || /*status*/
      o[4] === "complete" || /*show_progress*/
      o[6] === "hidden"), (!s || r[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && Y(
        e,
        "translucent",
        /*variant*/
        o[8] === "center" && /*status*/
        (o[4] === "pending" || /*status*/
        o[4] === "error") || /*translucent*/
        o[11] || /*show_progress*/
        o[6] === "minimal"
      ), (!s || r[0] & /*variant, show_progress, status*/
      336) && Y(
        e,
        "generating",
        /*status*/
        o[4] === "generating"
      ), (!s || r[0] & /*variant, show_progress, border*/
      4416) && Y(
        e,
        "border",
        /*border*/
        o[12]
      ), r[0] & /*absolute*/
      1024 && re(
        e,
        "position",
        /*absolute*/
        o[10] ? "absolute" : "static"
      ), r[0] & /*absolute*/
      1024 && re(
        e,
        "padding",
        /*absolute*/
        o[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(o) {
      s || (de(n), s = !0);
    },
    o(o) {
      me(n), s = !1;
    },
    d(o) {
      o && F(e), ~t && u[t].d(), l[33](null);
    }
  };
}
var Qn = function(l, e, t, n) {
  function i(s) {
    return s instanceof t ? s : new t(function(a) {
      a(s);
    });
  }
  return new (t || (t = Promise))(function(s, a) {
    function u(r) {
      try {
        o(n.next(r));
      } catch (c) {
        a(c);
      }
    }
    function f(r) {
      try {
        o(n.throw(r));
      } catch (c) {
        a(c);
      }
    }
    function o(r) {
      r.done ? s(r.value) : i(r.value).then(u, f);
    }
    o((n = n.apply(l, e || [])).next());
  });
};
let je = [], Ye = !1;
function Un(l) {
  return Qn(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (je.push(e), !Ye)
        Ye = !0;
      else
        return;
      yield jn(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < je.length; i++) {
          const a = je[i].getBoundingClientRect();
          (i === 0 || a.top + window.scrollY <= n[0]) && (n[0] = a.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), Ye = !1, je = [];
      });
    }
  });
}
function Wn(l, e, t) {
  let n, { $$slots: i = {}, $$scope: s } = e;
  this && this.__awaiter;
  const a = Bn();
  let { i18n: u } = e, { eta: f = null } = e, { queue_position: o } = e, { queue_size: r } = e, { status: c } = e, { scroll_to_output: b = !1 } = e, { timer: g = !0 } = e, { show_progress: v = "full" } = e, { message: M = null } = e, { progress: C = null } = e, { variant: I = "default" } = e, { loading_text: m = "Loading..." } = e, { absolute: d = !0 } = e, { translucent: q = !1 } = e, { border: A = !1 } = e, { autoscroll: p } = e, D, B = !1, E = 0, N = 0, z = null, H = null, Z = 0, O = null, $, V = null, ie = !0;
  const be = () => {
    t(0, f = t(27, z = t(19, _ = null))), t(25, E = performance.now()), t(26, N = 0), B = !0, fe();
  };
  function fe() {
    requestAnimationFrame(() => {
      t(26, N = (performance.now() - E) / 1e3), B && fe();
    });
  }
  function ae() {
    t(26, N = 0), t(0, f = t(27, z = t(19, _ = null))), B && (B = !1);
  }
  Pn(() => {
    B && ae();
  });
  let _ = null;
  function se(w) {
    dt[w ? "unshift" : "push"](() => {
      V = w, t(16, V), t(7, C), t(14, O), t(15, $);
    });
  }
  const Ve = () => {
    a("clear_status");
  };
  function Fe(w) {
    dt[w ? "unshift" : "push"](() => {
      D = w, t(13, D);
    });
  }
  return l.$$set = (w) => {
    "i18n" in w && t(1, u = w.i18n), "eta" in w && t(0, f = w.eta), "queue_position" in w && t(2, o = w.queue_position), "queue_size" in w && t(3, r = w.queue_size), "status" in w && t(4, c = w.status), "scroll_to_output" in w && t(22, b = w.scroll_to_output), "timer" in w && t(5, g = w.timer), "show_progress" in w && t(6, v = w.show_progress), "message" in w && t(23, M = w.message), "progress" in w && t(7, C = w.progress), "variant" in w && t(8, I = w.variant), "loading_text" in w && t(9, m = w.loading_text), "absolute" in w && t(10, d = w.absolute), "translucent" in w && t(11, q = w.translucent), "border" in w && t(12, A = w.border), "autoscroll" in w && t(24, p = w.autoscroll), "$$scope" in w && t(29, s = w.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (f === null && t(0, f = z), f != null && z !== f && (t(28, H = (performance.now() - E) / 1e3 + f), t(19, _ = H.toFixed(1)), t(27, z = f))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, Z = H === null || H <= 0 || !N ? null : Math.min(N / H, 1)), l.$$.dirty[0] & /*progress*/
    128 && C != null && t(18, ie = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (C != null ? t(14, O = C.map((w) => {
      if (w.index != null && w.length != null)
        return w.index / w.length;
      if (w.progress != null)
        return w.progress;
    })) : t(14, O = null), O ? (t(15, $ = O[O.length - 1]), V && ($ === 0 ? t(16, V.style.transition = "0", V) : t(16, V.style.transition = "150ms", V))) : t(15, $ = void 0)), l.$$.dirty[0] & /*status*/
    16 && (c === "pending" ? be() : ae()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && D && b && (c === "pending" || c === "complete") && Un(D, p), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = N.toFixed(1));
  }, [
    f,
    u,
    o,
    r,
    c,
    g,
    v,
    C,
    I,
    m,
    d,
    q,
    A,
    D,
    O,
    $,
    V,
    Z,
    ie,
    _,
    n,
    a,
    b,
    M,
    p,
    E,
    N,
    z,
    H,
    s,
    i,
    se,
    Ve,
    Fe
  ];
}
class xn extends Sn {
  constructor(e) {
    super(), Nn(
      this,
      e,
      Wn,
      Kn,
      In,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: $n,
  append: j,
  assign: ei,
  attr: k,
  binding_callbacks: ti,
  create_component: Ue,
  destroy_component: We,
  detach: ze,
  element: R,
  get_spread_object: li,
  get_spread_update: ni,
  init: ii,
  insert: Me,
  listen: T,
  mount_component: xe,
  run_all: fi,
  safe_not_equal: si,
  set_data: $e,
  set_input_value: ue,
  space: le,
  text: Ee,
  to_number: ye,
  toggle_class: zt,
  transition_in: et,
  transition_out: tt
} = window.__gradio__svelte__internal;
function oi(l) {
  let e;
  return {
    c() {
      e = Ee(
        /*label*/
        l[4]
      );
    },
    m(t, n) {
      Me(t, e, n);
    },
    p(t, n) {
      n[0] & /*label*/
      16 && $e(
        e,
        /*label*/
        t[4]
      );
    },
    d(t) {
      t && ze(e);
    }
  };
}
function ai(l) {
  let e, t, n, i, s, a, u, f, o, r, c, b, g, v, M, C, I, m, d, q, A, p, D, B, E, N, z, H, Z, O, $, V, ie, be, fe, ae, _, se, Ve;
  const Fe = [
    { autoscroll: (
      /*gradio*/
      l[0].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      l[0].i18n
    ) },
    /*loading_status*/
    l[14]
  ];
  let w = {};
  for (let h = 0; h < Fe.length; h += 1)
    w = ei(w, Fe[h]);
  return e = new xn({ props: w }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    l[26]
  ), s = new Jl({
    props: {
      show_label: (
        /*show_label*/
        l[12]
      ),
      info: (
        /*info*/
        l[5]
      ),
      $$slots: { default: [oi] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Ue(e.$$.fragment), t = le(), n = R("div"), i = R("div"), Ue(s.$$.fragment), a = le(), u = R("div"), f = R("input"), c = le(), b = R("input"), M = le(), C = R("button"), I = Ee("↺"), d = le(), q = R("div"), A = R("span"), p = Ee(
        /*minimum*/
        l[9]
      ), D = le(), B = R("div"), E = R("div"), N = le(), z = R("div"), H = le(), Z = R("input"), $ = le(), V = R("input"), be = le(), fe = R("span"), ae = Ee(
        /*maximum*/
        l[10]
      ), k(f, "aria-label", o = `min input for ${/*label*/
      l[4]}`), k(f, "data-testid", "min-input"), k(f, "type", "number"), k(
        f,
        "min",
        /*minimum*/
        l[9]
      ), k(
        f,
        "max",
        /*maximum*/
        l[10]
      ), f.disabled = r = !/*interactive*/
      l[13], k(f, "class", "svelte-17pocne"), k(b, "aria-label", g = `max input for ${/*label*/
      l[4]}`), k(b, "data-testid", "max-input"), k(b, "type", "number"), k(
        b,
        "min",
        /*minimum*/
        l[9]
      ), k(
        b,
        "max",
        /*maximum*/
        l[10]
      ), b.disabled = v = !/*interactive*/
      l[13], k(b, "class", "svelte-17pocne"), k(C, "class", "reset-button svelte-17pocne"), C.disabled = m = !/*interactive*/
      l[13], k(C, "aria-label", "Reset to default value"), k(u, "class", "tab-like-container svelte-17pocne"), k(i, "class", "head svelte-17pocne"), k(n, "class", "wrap svelte-17pocne"), k(A, "class", "min_value svelte-17pocne"), k(E, "class", "range-bg svelte-17pocne"), k(z, "class", "range-line svelte-17pocne"), k(
        z,
        "style",
        /*rangeLine*/
        l[18]
      ), zt(z, "disabled", !/*interactive*/
      l[13]), k(Z, "type", "range"), Z.disabled = O = !/*interactive*/
      l[13], k(
        Z,
        "min",
        /*minimum*/
        l[9]
      ), k(
        Z,
        "max",
        /*maximum*/
        l[10]
      ), k(
        Z,
        "step",
        /*step*/
        l[11]
      ), k(Z, "class", "svelte-17pocne"), k(V, "type", "range"), V.disabled = ie = !/*interactive*/
      l[13], k(
        V,
        "min",
        /*minimum*/
        l[9]
      ), k(
        V,
        "max",
        /*maximum*/
        l[10]
      ), k(
        V,
        "step",
        /*step*/
        l[11]
      ), k(V, "class", "svelte-17pocne"), k(B, "class", "range-slider svelte-17pocne"), k(fe, "class", "max_value svelte-17pocne"), k(q, "class", "slider_input_container svelte-17pocne");
    },
    m(h, y) {
      xe(e, h, y), Me(h, t, y), Me(h, n, y), j(n, i), xe(s, i, null), j(i, a), j(i, u), j(u, f), ue(
        f,
        /*selected_min*/
        l[15]
      ), j(u, c), j(u, b), ue(
        b,
        /*selected_max*/
        l[16]
      ), j(u, M), j(u, C), j(C, I), Me(h, d, y), Me(h, q, y), j(q, A), j(A, p), j(q, D), j(q, B), j(B, E), j(B, N), j(B, z), l[29](z), j(B, H), j(B, Z), ue(
        Z,
        /*selected_min*/
        l[15]
      ), j(B, $), j(B, V), ue(
        V,
        /*selected_max*/
        l[16]
      ), j(q, be), j(q, fe), j(fe, ae), _ = !0, se || (Ve = [
        T(
          f,
          "input",
          /*input0_input_handler*/
          l[27]
        ),
        T(
          f,
          "pointerup",
          /*handle_release*/
          l[21]
        ),
        T(
          f,
          "blur",
          /*handle_release*/
          l[21]
        ),
        T(
          b,
          "input",
          /*input1_input_handler*/
          l[28]
        ),
        T(
          b,
          "pointerup",
          /*handle_release*/
          l[21]
        ),
        T(
          b,
          "blur",
          /*handle_release*/
          l[21]
        ),
        T(
          C,
          "click",
          /*reset_value*/
          l[22]
        ),
        T(
          Z,
          "change",
          /*input2_change_input_handler*/
          l[30]
        ),
        T(
          Z,
          "input",
          /*input2_change_input_handler*/
          l[30]
        ),
        T(
          Z,
          "input",
          /*handle_min_change*/
          l[19]
        ),
        T(
          Z,
          "pointerup",
          /*handle_release*/
          l[21]
        ),
        T(
          V,
          "change",
          /*input3_change_input_handler*/
          l[31]
        ),
        T(
          V,
          "input",
          /*input3_change_input_handler*/
          l[31]
        ),
        T(
          V,
          "input",
          /*handle_max_change*/
          l[20]
        ),
        T(
          V,
          "pointerup",
          /*handle_release*/
          l[21]
        )
      ], se = !0);
    },
    p(h, y) {
      const ge = y[0] & /*gradio, loading_status*/
      16385 ? ni(Fe, [
        y[0] & /*gradio*/
        1 && { autoscroll: (
          /*gradio*/
          h[0].autoscroll
        ) },
        y[0] & /*gradio*/
        1 && { i18n: (
          /*gradio*/
          h[0].i18n
        ) },
        y[0] & /*loading_status*/
        16384 && li(
          /*loading_status*/
          h[14]
        )
      ]) : {};
      e.$set(ge);
      const he = {};
      y[0] & /*show_label*/
      4096 && (he.show_label = /*show_label*/
      h[12]), y[0] & /*info*/
      32 && (he.info = /*info*/
      h[5]), y[0] & /*label*/
      16 | y[1] & /*$$scope*/
      8 && (he.$$scope = { dirty: y, ctx: h }), s.$set(he), (!_ || y[0] & /*label*/
      16 && o !== (o = `min input for ${/*label*/
      h[4]}`)) && k(f, "aria-label", o), (!_ || y[0] & /*minimum*/
      512) && k(
        f,
        "min",
        /*minimum*/
        h[9]
      ), (!_ || y[0] & /*maximum*/
      1024) && k(
        f,
        "max",
        /*maximum*/
        h[10]
      ), (!_ || y[0] & /*interactive*/
      8192 && r !== (r = !/*interactive*/
      h[13])) && (f.disabled = r), y[0] & /*selected_min*/
      32768 && ye(f.value) !== /*selected_min*/
      h[15] && ue(
        f,
        /*selected_min*/
        h[15]
      ), (!_ || y[0] & /*label*/
      16 && g !== (g = `max input for ${/*label*/
      h[4]}`)) && k(b, "aria-label", g), (!_ || y[0] & /*minimum*/
      512) && k(
        b,
        "min",
        /*minimum*/
        h[9]
      ), (!_ || y[0] & /*maximum*/
      1024) && k(
        b,
        "max",
        /*maximum*/
        h[10]
      ), (!_ || y[0] & /*interactive*/
      8192 && v !== (v = !/*interactive*/
      h[13])) && (b.disabled = v), y[0] & /*selected_max*/
      65536 && ye(b.value) !== /*selected_max*/
      h[16] && ue(
        b,
        /*selected_max*/
        h[16]
      ), (!_ || y[0] & /*interactive*/
      8192 && m !== (m = !/*interactive*/
      h[13])) && (C.disabled = m), (!_ || y[0] & /*minimum*/
      512) && $e(
        p,
        /*minimum*/
        h[9]
      ), (!_ || y[0] & /*rangeLine*/
      262144) && k(
        z,
        "style",
        /*rangeLine*/
        h[18]
      ), (!_ || y[0] & /*interactive*/
      8192) && zt(z, "disabled", !/*interactive*/
      h[13]), (!_ || y[0] & /*interactive*/
      8192 && O !== (O = !/*interactive*/
      h[13])) && (Z.disabled = O), (!_ || y[0] & /*minimum*/
      512) && k(
        Z,
        "min",
        /*minimum*/
        h[9]
      ), (!_ || y[0] & /*maximum*/
      1024) && k(
        Z,
        "max",
        /*maximum*/
        h[10]
      ), (!_ || y[0] & /*step*/
      2048) && k(
        Z,
        "step",
        /*step*/
        h[11]
      ), y[0] & /*selected_min*/
      32768 && ue(
        Z,
        /*selected_min*/
        h[15]
      ), (!_ || y[0] & /*interactive*/
      8192 && ie !== (ie = !/*interactive*/
      h[13])) && (V.disabled = ie), (!_ || y[0] & /*minimum*/
      512) && k(
        V,
        "min",
        /*minimum*/
        h[9]
      ), (!_ || y[0] & /*maximum*/
      1024) && k(
        V,
        "max",
        /*maximum*/
        h[10]
      ), (!_ || y[0] & /*step*/
      2048) && k(
        V,
        "step",
        /*step*/
        h[11]
      ), y[0] & /*selected_max*/
      65536 && ue(
        V,
        /*selected_max*/
        h[16]
      ), (!_ || y[0] & /*maximum*/
      1024) && $e(
        ae,
        /*maximum*/
        h[10]
      );
    },
    i(h) {
      _ || (et(e.$$.fragment, h), et(s.$$.fragment, h), _ = !0);
    },
    o(h) {
      tt(e.$$.fragment, h), tt(s.$$.fragment, h), _ = !1;
    },
    d(h) {
      h && (ze(t), ze(n), ze(d), ze(q)), We(e, h), We(s), l[29](null), se = !1, fi(Ve);
    }
  };
}
function ui(l) {
  let e, t;
  return e = new fl({
    props: {
      visible: (
        /*visible*/
        l[3]
      ),
      elem_id: (
        /*elem_id*/
        l[1]
      ),
      elem_classes: (
        /*elem_classes*/
        l[2]
      ),
      container: (
        /*container*/
        l[6]
      ),
      scale: (
        /*scale*/
        l[7]
      ),
      min_width: (
        /*min_width*/
        l[8]
      ),
      $$slots: { default: [ai] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Ue(e.$$.fragment);
    },
    m(n, i) {
      xe(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i[0] & /*visible*/
      8 && (s.visible = /*visible*/
      n[3]), i[0] & /*elem_id*/
      2 && (s.elem_id = /*elem_id*/
      n[1]), i[0] & /*elem_classes*/
      4 && (s.elem_classes = /*elem_classes*/
      n[2]), i[0] & /*container*/
      64 && (s.container = /*container*/
      n[6]), i[0] & /*scale*/
      128 && (s.scale = /*scale*/
      n[7]), i[0] & /*min_width*/
      256 && (s.min_width = /*min_width*/
      n[8]), i[0] & /*maximum, interactive, minimum, step, selected_max, selected_min, rangeLine, range_input, label, show_label, info, gradio, loading_status*/
      523825 | i[1] & /*$$scope*/
      8 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (et(e.$$.fragment, n), t = !0);
    },
    o(n) {
      tt(e.$$.fragment, n), t = !1;
    },
    d(n) {
      We(e, n);
    }
  };
}
function ri(l, e, t) {
  let n, { gradio: i } = e, { elem_id: s = "" } = e, { elem_classes: a = [] } = e, { visible: u = !0 } = e, { value: f } = e, { label: o = i.i18n("slider.slider") } = e, { info: r = void 0 } = e, { container: c = !0 } = e, { scale: b = null } = e, { min_width: g = void 0 } = e, { minimum: v = 0 } = e, { maximum: M = 100 } = e, { step: C } = e, { show_label: I } = e, { interactive: m } = e, { loading_status: d } = e, { value_is_output: q = !1 } = e;
  function A(_, se) {
    t(23, f = [_, se]), i.dispatch("change", [_, se]), q || i.dispatch("input", [_, se]);
  }
  function p(_) {
    t(15, N = parseFloat(_.target.value)), N > z && t(16, z = N);
  }
  function D(_) {
    t(16, z = parseFloat(_.target.value)), z < N && t(15, N = z);
  }
  function B(_) {
    i.dispatch("release", f);
  }
  let E = f, [N, z] = f, H = f, Z;
  function O() {
    t(15, [N, z] = H, N, (t(16, z), t(25, E), t(23, f))), i.dispatch("change"), i.dispatch("release", f);
  }
  const $ = () => i.dispatch("clear_status", d);
  function V() {
    N = ye(this.value), t(15, N), t(25, E), t(23, f);
  }
  function ie() {
    z = ye(this.value), t(16, z), t(25, E), t(23, f);
  }
  function be(_) {
    ti[_ ? "unshift" : "push"](() => {
      Z = _, t(17, Z);
    });
  }
  function fe() {
    N = ye(this.value), t(15, N), t(25, E), t(23, f);
  }
  function ae() {
    z = ye(this.value), t(16, z), t(25, E), t(23, f);
  }
  return l.$$set = (_) => {
    "gradio" in _ && t(0, i = _.gradio), "elem_id" in _ && t(1, s = _.elem_id), "elem_classes" in _ && t(2, a = _.elem_classes), "visible" in _ && t(3, u = _.visible), "value" in _ && t(23, f = _.value), "label" in _ && t(4, o = _.label), "info" in _ && t(5, r = _.info), "container" in _ && t(6, c = _.container), "scale" in _ && t(7, b = _.scale), "min_width" in _ && t(8, g = _.min_width), "minimum" in _ && t(9, v = _.minimum), "maximum" in _ && t(10, M = _.maximum), "step" in _ && t(11, C = _.step), "show_label" in _ && t(12, I = _.show_label), "interactive" in _ && t(13, m = _.interactive), "loading_status" in _ && t(14, d = _.loading_status), "value_is_output" in _ && t(24, q = _.value_is_output);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*old_value, value*/
    41943040 && JSON.stringify(E) !== JSON.stringify(f) && (t(15, [N, z] = f, N, (t(16, z), t(25, E), t(23, f))), t(25, E = f)), l.$$.dirty[0] & /*selected_min, selected_max*/
    98304 && A(N, z), l.$$.dirty[0] & /*selected_min, minimum, maximum, selected_max*/
    99840 && t(18, n = `
      left: ${(N - v) / (M - v) * 100}%;
      width: ${(z - N) / (M - v) * 100}%;
    `);
  }, [
    i,
    s,
    a,
    u,
    o,
    r,
    c,
    b,
    g,
    v,
    M,
    C,
    I,
    m,
    d,
    N,
    z,
    Z,
    n,
    p,
    D,
    B,
    O,
    f,
    q,
    E,
    $,
    V,
    ie,
    be,
    fe,
    ae
  ];
}
class _i extends $n {
  constructor(e) {
    super(), ii(
      this,
      e,
      ri,
      ui,
      si,
      {
        gradio: 0,
        elem_id: 1,
        elem_classes: 2,
        visible: 3,
        value: 23,
        label: 4,
        info: 5,
        container: 6,
        scale: 7,
        min_width: 8,
        minimum: 9,
        maximum: 10,
        step: 11,
        show_label: 12,
        interactive: 13,
        loading_status: 14,
        value_is_output: 24
      },
      null,
      [-1, -1]
    );
  }
}
export {
  _i as default
};
