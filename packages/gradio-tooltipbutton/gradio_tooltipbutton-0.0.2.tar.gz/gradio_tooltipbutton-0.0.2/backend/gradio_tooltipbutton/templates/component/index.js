const {
  SvelteComponent: O,
  append: v,
  attr: u,
  bubble: P,
  check_outros: Q,
  create_slot: D,
  detach: w,
  element: h,
  empty: R,
  get_all_dirty_from_scope: E,
  get_slot_changes: F,
  group_outros: T,
  init: U,
  insert: g,
  listen: W,
  safe_not_equal: X,
  set_data: G,
  set_style: k,
  space: H,
  src_url_equal: M,
  svg_element: V,
  text: J,
  toggle_class: z,
  transition_in: Z,
  transition_out: S,
  update_slot_base: K
} = window.__gradio__svelte__internal;
function Y(i) {
  let e, l, n, t, f, o, C, s = (
    /*icon*/
    i[7] && L(i)
  );
  const _ = (
    /*#slots*/
    i[13].default
  ), a = D(
    _,
    i,
    /*$$scope*/
    i[12],
    null
  );
  let c = (
    /*tooltip*/
    i[11] && I(i)
  );
  return {
    c() {
      e = h("button"), s && s.c(), l = H(), a && a.c(), n = H(), c && c.c(), u(e, "class", t = "button-wrapper " + /*size*/
      i[4] + " " + /*variant*/
      i[3] + " " + /*elem_classes*/
      i[1].join(" ") + " svelte-kqcdno"), u(
        e,
        "id",
        /*elem_id*/
        i[0]
      ), e.disabled = /*disabled*/
      i[8], z(e, "hidden", !/*visible*/
      i[2]), k(
        e,
        "flex-grow",
        /*scale*/
        i[9]
      ), k(
        e,
        "width",
        /*scale*/
        i[9] === 0 ? "fit-content" : null
      ), k(e, "min-width", typeof /*min_width*/
      i[10] == "number" ? `calc(min(${/*min_width*/
      i[10]}px, 100%))` : null);
    },
    m(m, b) {
      g(m, e, b), s && s.m(e, null), v(e, l), a && a.m(e, null), v(e, n), c && c.m(e, null), f = !0, o || (C = W(
        e,
        "click",
        /*click_handler*/
        i[14]
      ), o = !0);
    },
    p(m, b) {
      /*icon*/
      m[7] ? s ? s.p(m, b) : (s = L(m), s.c(), s.m(e, l)) : s && (s.d(1), s = null), a && a.p && (!f || b & /*$$scope*/
      4096) && K(
        a,
        _,
        m,
        /*$$scope*/
        m[12],
        f ? F(
          _,
          /*$$scope*/
          m[12],
          b,
          null
        ) : E(
          /*$$scope*/
          m[12]
        ),
        null
      ), /*tooltip*/
      m[11] ? c ? c.p(m, b) : (c = I(m), c.c(), c.m(e, null)) : c && (c.d(1), c = null), (!f || b & /*size, variant, elem_classes*/
      26 && t !== (t = "button-wrapper " + /*size*/
      m[4] + " " + /*variant*/
      m[3] + " " + /*elem_classes*/
      m[1].join(" ") + " svelte-kqcdno")) && u(e, "class", t), (!f || b & /*elem_id*/
      1) && u(
        e,
        "id",
        /*elem_id*/
        m[0]
      ), (!f || b & /*disabled*/
      256) && (e.disabled = /*disabled*/
      m[8]), (!f || b & /*size, variant, elem_classes, visible*/
      30) && z(e, "hidden", !/*visible*/
      m[2]), b & /*scale*/
      512 && k(
        e,
        "flex-grow",
        /*scale*/
        m[9]
      ), b & /*scale*/
      512 && k(
        e,
        "width",
        /*scale*/
        m[9] === 0 ? "fit-content" : null
      ), b & /*min_width*/
      1024 && k(e, "min-width", typeof /*min_width*/
      m[10] == "number" ? `calc(min(${/*min_width*/
      m[10]}px, 100%))` : null);
    },
    i(m) {
      f || (Z(a, m), f = !0);
    },
    o(m) {
      S(a, m), f = !1;
    },
    d(m) {
      m && w(e), s && s.d(), a && a.d(m), c && c.d(), o = !1, C();
    }
  };
}
function y(i) {
  let e, l, n, t, f, o = (
    /*icon*/
    i[7] && N(i)
  );
  const C = (
    /*#slots*/
    i[13].default
  ), s = D(
    C,
    i,
    /*$$scope*/
    i[12],
    null
  );
  let _ = (
    /*tooltip*/
    i[11] && A(i)
  );
  return {
    c() {
      e = h("a"), o && o.c(), l = H(), s && s.c(), n = H(), _ && _.c(), u(
        e,
        "href",
        /*link*/
        i[6]
      ), u(e, "rel", "noopener noreferrer"), u(
        e,
        "aria-disabled",
        /*disabled*/
        i[8]
      ), u(e, "class", t = "button-wrapper " + /*size*/
      i[4] + " " + /*variant*/
      i[3] + " " + /*elem_classes*/
      i[1].join(" ") + " svelte-kqcdno"), u(
        e,
        "id",
        /*elem_id*/
        i[0]
      ), z(e, "hidden", !/*visible*/
      i[2]), z(
        e,
        "disabled",
        /*disabled*/
        i[8]
      ), k(
        e,
        "flex-grow",
        /*scale*/
        i[9]
      ), k(
        e,
        "pointer-events",
        /*disabled*/
        i[8] ? "none" : null
      ), k(
        e,
        "width",
        /*scale*/
        i[9] === 0 ? "fit-content" : null
      ), k(e, "min-width", typeof /*min_width*/
      i[10] == "number" ? `calc(min(${/*min_width*/
      i[10]}px, 100%))` : null);
    },
    m(a, c) {
      g(a, e, c), o && o.m(e, null), v(e, l), s && s.m(e, null), v(e, n), _ && _.m(e, null), f = !0;
    },
    p(a, c) {
      /*icon*/
      a[7] ? o ? o.p(a, c) : (o = N(a), o.c(), o.m(e, l)) : o && (o.d(1), o = null), s && s.p && (!f || c & /*$$scope*/
      4096) && K(
        s,
        C,
        a,
        /*$$scope*/
        a[12],
        f ? F(
          C,
          /*$$scope*/
          a[12],
          c,
          null
        ) : E(
          /*$$scope*/
          a[12]
        ),
        null
      ), /*tooltip*/
      a[11] ? _ ? _.p(a, c) : (_ = A(a), _.c(), _.m(e, null)) : _ && (_.d(1), _ = null), (!f || c & /*link*/
      64) && u(
        e,
        "href",
        /*link*/
        a[6]
      ), (!f || c & /*disabled*/
      256) && u(
        e,
        "aria-disabled",
        /*disabled*/
        a[8]
      ), (!f || c & /*size, variant, elem_classes*/
      26 && t !== (t = "button-wrapper " + /*size*/
      a[4] + " " + /*variant*/
      a[3] + " " + /*elem_classes*/
      a[1].join(" ") + " svelte-kqcdno")) && u(e, "class", t), (!f || c & /*elem_id*/
      1) && u(
        e,
        "id",
        /*elem_id*/
        a[0]
      ), (!f || c & /*size, variant, elem_classes, visible*/
      30) && z(e, "hidden", !/*visible*/
      a[2]), (!f || c & /*size, variant, elem_classes, disabled*/
      282) && z(
        e,
        "disabled",
        /*disabled*/
        a[8]
      ), c & /*scale*/
      512 && k(
        e,
        "flex-grow",
        /*scale*/
        a[9]
      ), c & /*disabled*/
      256 && k(
        e,
        "pointer-events",
        /*disabled*/
        a[8] ? "none" : null
      ), c & /*scale*/
      512 && k(
        e,
        "width",
        /*scale*/
        a[9] === 0 ? "fit-content" : null
      ), c & /*min_width*/
      1024 && k(e, "min-width", typeof /*min_width*/
      a[10] == "number" ? `calc(min(${/*min_width*/
      a[10]}px, 100%))` : null);
    },
    i(a) {
      f || (Z(s, a), f = !0);
    },
    o(a) {
      S(s, a), f = !1;
    },
    d(a) {
      a && w(e), o && o.d(), s && s.d(a), _ && _.d();
    }
  };
}
function L(i) {
  let e, l, n;
  return {
    c() {
      e = h("img"), u(e, "class", "button-icon svelte-kqcdno"), M(e.src, l = /*icon*/
      i[7].url) || u(e, "src", l), u(e, "alt", n = `${/*value*/
      i[5]} icon`);
    },
    m(t, f) {
      g(t, e, f);
    },
    p(t, f) {
      f & /*icon*/
      128 && !M(e.src, l = /*icon*/
      t[7].url) && u(e, "src", l), f & /*value*/
      32 && n !== (n = `${/*value*/
      t[5]} icon`) && u(e, "alt", n);
    },
    d(t) {
      t && w(e);
    }
  };
}
function I(i) {
  let e, l, n, t, f, o, C;
  return {
    c() {
      e = h("div"), l = V("svg"), n = V("circle"), t = V("path"), f = H(), o = h("span"), C = J(
        /*tooltip*/
        i[11]
      ), u(n, "cx", "7.5"), u(n, "cy", "7.5"), u(n, "r", "7"), u(n, "fill", "white"), u(n, "stroke", "#CCCCCC"), u(t, "d", "M7.88597 8.71201H6.71997V8.39301C6.71997 8.11434 6.76397 7.87601 6.85197 7.67801C6.94731 7.47267 7.06464 7.29667 7.20397 7.15001C7.35064 7.00334 7.50464 6.86767 7.66597 6.74301C7.82731 6.61834 7.97764 6.49734 8.11697 6.38001C8.26364 6.26267 8.38097 6.13434 8.46897 5.99501C8.56431 5.85567 8.61197 5.69067 8.61197 5.50001C8.61197 5.26534 8.52764 5.07467 8.35897 4.92801C8.19764 4.77401 7.93364 4.69701 7.56697 4.69701C7.24431 4.69701 6.95831 4.77034 6.70897 4.91701C6.45964 5.05634 6.27264 5.27267 6.14797 5.56601C6.03064 5.85934 6.00131 6.22967 6.05997 6.67701L5.01497 5.92901C4.96364 5.45967 5.04431 5.04534 5.25697 4.68601C5.47697 4.32667 5.79231 4.04434 6.20297 3.83901C6.62097 3.63367 7.10497 3.53101 7.65497 3.53101C8.35897 3.53101 8.91631 3.68134 9.32697 3.98201C9.74497 4.28267 9.95397 4.74834 9.95397 5.37901C9.95397 5.65767 9.90264 5.89967 9.79997 6.10501C9.70464 6.30301 9.57631 6.47901 9.41497 6.63301C9.26097 6.78701 9.09597 6.93001 8.91997 7.06201C8.74397 7.18667 8.57531 7.31867 8.41397 7.45801C8.25997 7.59001 8.13164 7.74034 8.02897 7.90901C7.93364 8.07034 7.88597 8.26467 7.88597 8.49201V8.71201ZM7.99597 11H6.58797V9.43801H7.99597V11Z"), u(t, "fill", "#CCCCCC"), u(l, "xmlns", "http://www.w3.org/2000/svg"), u(l, "width", "15"), u(l, "height", "15"), u(l, "viewBox", "0 0 15 15"), u(l, "fill", "none"), u(l, "class", "question-mark svelte-kqcdno"), u(o, "class", "tooltip svelte-kqcdno"), u(e, "class", "tooltip-wrapper svelte-kqcdno");
    },
    m(s, _) {
      g(s, e, _), v(e, l), v(l, n), v(l, t), v(e, f), v(e, o), v(o, C);
    },
    p(s, _) {
      _ & /*tooltip*/
      2048 && G(
        C,
        /*tooltip*/
        s[11]
      );
    },
    d(s) {
      s && w(e);
    }
  };
}
function N(i) {
  let e, l, n;
  return {
    c() {
      e = h("img"), u(e, "class", "button-icon svelte-kqcdno"), M(e.src, l = /*icon*/
      i[7].url) || u(e, "src", l), u(e, "alt", n = `${/*value*/
      i[5]} icon`);
    },
    m(t, f) {
      g(t, e, f);
    },
    p(t, f) {
      f & /*icon*/
      128 && !M(e.src, l = /*icon*/
      t[7].url) && u(e, "src", l), f & /*value*/
      32 && n !== (n = `${/*value*/
      t[5]} icon`) && u(e, "alt", n);
    },
    d(t) {
      t && w(e);
    }
  };
}
function A(i) {
  let e, l, n, t, f, o, C;
  return {
    c() {
      e = h("div"), l = V("svg"), n = V("circle"), t = V("path"), f = H(), o = h("span"), C = J(
        /*tooltip*/
        i[11]
      ), u(n, "cx", "7.5"), u(n, "cy", "7.5"), u(n, "r", "7"), u(n, "fill", "white"), u(n, "stroke", "#CCCCCC"), u(t, "d", "M7.88597 8.71201H6.71997V8.39301C6.71997 8.11434 6.76397 7.87601 6.85197 7.67801C6.94731 7.47267 7.06464 7.29667 7.20397 7.15001C7.35064 7.00334 7.50464 6.86767 7.66597 6.74301C7.82731 6.61834 7.97764 6.49734 8.11697 6.38001C8.26364 6.26267 8.38097 6.13434 8.46897 5.99501C8.56431 5.85567 8.61197 5.69067 8.61197 5.50001C8.61197 5.26534 8.52764 5.07467 8.35897 4.92801C8.19764 4.77401 7.93364 4.69701 7.56697 4.69701C7.24431 4.69701 6.95831 4.77034 6.70897 4.91701C6.45964 5.05634 6.27264 5.27267 6.14797 5.56601C6.03064 5.85934 6.00131 6.22967 6.05997 6.67701L5.01497 5.92901C4.96364 5.45967 5.04431 5.04534 5.25697 4.68601C5.47697 4.32667 5.79231 4.04434 6.20297 3.83901C6.62097 3.63367 7.10497 3.53101 7.65497 3.53101C8.35897 3.53101 8.91631 3.68134 9.32697 3.98201C9.74497 4.28267 9.95397 4.74834 9.95397 5.37901C9.95397 5.65767 9.90264 5.89967 9.79997 6.10501C9.70464 6.30301 9.57631 6.47901 9.41497 6.63301C9.26097 6.78701 9.09597 6.93001 8.91997 7.06201C8.74397 7.18667 8.57531 7.31867 8.41397 7.45801C8.25997 7.59001 8.13164 7.74034 8.02897 7.90901C7.93364 8.07034 7.88597 8.26467 7.88597 8.49201V8.71201ZM7.99597 11H6.58797V9.43801H7.99597V11Z"), u(t, "fill", "#CCCCCC"), u(l, "xmlns", "http://www.w3.org/2000/svg"), u(l, "width", "15"), u(l, "height", "15"), u(l, "viewBox", "0 0 15 15"), u(l, "fill", "none"), u(l, "class", "question-mark svelte-kqcdno"), u(o, "class", "tooltip svelte-kqcdno"), u(e, "class", "tooltip-wrapper svelte-kqcdno");
    },
    m(s, _) {
      g(s, e, _), v(e, l), v(l, n), v(l, t), v(e, f), v(e, o), v(o, C);
    },
    p(s, _) {
      _ & /*tooltip*/
      2048 && G(
        C,
        /*tooltip*/
        s[11]
      );
    },
    d(s) {
      s && w(e);
    }
  };
}
function p(i) {
  let e, l, n, t;
  const f = [y, Y], o = [];
  function C(s, _) {
    return (
      /*link*/
      s[6] && /*link*/
      s[6].length > 0 ? 0 : 1
    );
  }
  return e = C(i), l = o[e] = f[e](i), {
    c() {
      l.c(), n = R();
    },
    m(s, _) {
      o[e].m(s, _), g(s, n, _), t = !0;
    },
    p(s, [_]) {
      let a = e;
      e = C(s), e === a ? o[e].p(s, _) : (T(), S(o[a], 1, 1, () => {
        o[a] = null;
      }), Q(), l = o[e], l ? l.p(s, _) : (l = o[e] = f[e](s), l.c()), Z(l, 1), l.m(n.parentNode, n));
    },
    i(s) {
      t || (Z(l), t = !0);
    },
    o(s) {
      S(l), t = !1;
    },
    d(s) {
      s && w(n), o[e].d(s);
    }
  };
}
function x(i, e, l) {
  let { $$slots: n = {}, $$scope: t } = e, { elem_id: f = "" } = e, { elem_classes: o = [] } = e, { visible: C = !0 } = e, { variant: s = "secondary" } = e, { size: _ = "lg" } = e, { value: a = null } = e, { link: c = null } = e, { icon: m = null } = e, { disabled: b = !1 } = e, { scale: B = null } = e, { min_width: q = void 0 } = e, { tooltip: j = "" } = e;
  function d(r) {
    P.call(this, i, r);
  }
  return i.$$set = (r) => {
    "elem_id" in r && l(0, f = r.elem_id), "elem_classes" in r && l(1, o = r.elem_classes), "visible" in r && l(2, C = r.visible), "variant" in r && l(3, s = r.variant), "size" in r && l(4, _ = r.size), "value" in r && l(5, a = r.value), "link" in r && l(6, c = r.link), "icon" in r && l(7, m = r.icon), "disabled" in r && l(8, b = r.disabled), "scale" in r && l(9, B = r.scale), "min_width" in r && l(10, q = r.min_width), "tooltip" in r && l(11, j = r.tooltip), "$$scope" in r && l(12, t = r.$$scope);
  }, [
    f,
    o,
    C,
    s,
    _,
    a,
    c,
    m,
    b,
    B,
    q,
    j,
    t,
    n,
    d
  ];
}
class $ extends O {
  constructor(e) {
    super(), U(this, e, x, p, X, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10,
      tooltip: 11
    });
  }
}
const {
  SvelteComponent: ee,
  create_component: le,
  destroy_component: ie,
  detach: ne,
  init: te,
  insert: fe,
  mount_component: se,
  safe_not_equal: ae,
  set_data: ue,
  text: oe,
  transition_in: _e,
  transition_out: ce
} = window.__gradio__svelte__internal;
function me(i) {
  let e = (
    /*value*/
    (i[3] ? (
      /*gradio*/
      i[12].i18n(
        /*value*/
        i[3]
      )
    ) : "") + ""
  ), l;
  return {
    c() {
      l = oe(e);
    },
    m(n, t) {
      fe(n, l, t);
    },
    p(n, t) {
      t & /*value, gradio*/
      4104 && e !== (e = /*value*/
      (n[3] ? (
        /*gradio*/
        n[12].i18n(
          /*value*/
          n[3]
        )
      ) : "") + "") && ue(l, e);
    },
    d(n) {
      n && ne(l);
    }
  };
}
function de(i) {
  let e, l;
  return e = new $({
    props: {
      value: (
        /*value*/
        i[3]
      ),
      variant: (
        /*variant*/
        i[4]
      ),
      elem_id: (
        /*elem_id*/
        i[0]
      ),
      elem_classes: (
        /*elem_classes*/
        i[1]
      ),
      size: (
        /*size*/
        i[6]
      ),
      scale: (
        /*scale*/
        i[7]
      ),
      link: (
        /*link*/
        i[9]
      ),
      icon: (
        /*icon*/
        i[8]
      ),
      min_width: (
        /*min_width*/
        i[10]
      ),
      tooltip: (
        /*tooltip*/
        i[11]
      ),
      visible: (
        /*visible*/
        i[2]
      ),
      disabled: !/*interactive*/
      i[5],
      $$slots: { default: [me] },
      $$scope: { ctx: i }
    }
  }), e.$on(
    "click",
    /*click_handler*/
    i[13]
  ), {
    c() {
      le(e.$$.fragment);
    },
    m(n, t) {
      se(e, n, t), l = !0;
    },
    p(n, [t]) {
      const f = {};
      t & /*value*/
      8 && (f.value = /*value*/
      n[3]), t & /*variant*/
      16 && (f.variant = /*variant*/
      n[4]), t & /*elem_id*/
      1 && (f.elem_id = /*elem_id*/
      n[0]), t & /*elem_classes*/
      2 && (f.elem_classes = /*elem_classes*/
      n[1]), t & /*size*/
      64 && (f.size = /*size*/
      n[6]), t & /*scale*/
      128 && (f.scale = /*scale*/
      n[7]), t & /*link*/
      512 && (f.link = /*link*/
      n[9]), t & /*icon*/
      256 && (f.icon = /*icon*/
      n[8]), t & /*min_width*/
      1024 && (f.min_width = /*min_width*/
      n[10]), t & /*tooltip*/
      2048 && (f.tooltip = /*tooltip*/
      n[11]), t & /*visible*/
      4 && (f.visible = /*visible*/
      n[2]), t & /*interactive*/
      32 && (f.disabled = !/*interactive*/
      n[5]), t & /*$$scope, value, gradio*/
      20488 && (f.$$scope = { dirty: t, ctx: n }), e.$set(f);
    },
    i(n) {
      l || (_e(e.$$.fragment, n), l = !0);
    },
    o(n) {
      ce(e.$$.fragment, n), l = !1;
    },
    d(n) {
      ie(e, n);
    }
  };
}
function re(i, e, l) {
  let { elem_id: n = "" } = e, { elem_classes: t = [] } = e, { visible: f = !0 } = e, { value: o } = e, { variant: C = "secondary" } = e, { interactive: s } = e, { size: _ = "lg" } = e, { scale: a = null } = e, { icon: c = null } = e, { link: m = null } = e, { min_width: b = void 0 } = e, { tooltip: B = "" } = e, { gradio: q } = e;
  const j = () => q.dispatch("click");
  return i.$$set = (d) => {
    "elem_id" in d && l(0, n = d.elem_id), "elem_classes" in d && l(1, t = d.elem_classes), "visible" in d && l(2, f = d.visible), "value" in d && l(3, o = d.value), "variant" in d && l(4, C = d.variant), "interactive" in d && l(5, s = d.interactive), "size" in d && l(6, _ = d.size), "scale" in d && l(7, a = d.scale), "icon" in d && l(8, c = d.icon), "link" in d && l(9, m = d.link), "min_width" in d && l(10, b = d.min_width), "tooltip" in d && l(11, B = d.tooltip), "gradio" in d && l(12, q = d.gradio);
  }, [
    n,
    t,
    f,
    o,
    C,
    s,
    _,
    a,
    c,
    m,
    b,
    B,
    q,
    j
  ];
}
class Ce extends ee {
  constructor(e) {
    super(), te(this, e, re, de, ae, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      value: 3,
      variant: 4,
      interactive: 5,
      size: 6,
      scale: 7,
      icon: 8,
      link: 9,
      min_width: 10,
      tooltip: 11,
      gradio: 12
    });
  }
}
export {
  $ as BaseButton,
  Ce as default
};
