const {
  SvelteComponent: ce,
  assign: se,
  create_slot: _e,
  detach: de,
  element: re,
  get_all_dirty_from_scope: ue,
  get_slot_changes: me,
  get_spread_update: be,
  init: ge,
  insert: he,
  safe_not_equal: we,
  set_dynamic_element_data: P,
  set_style: y,
  toggle_class: L,
  transition_in: Z,
  transition_out: p,
  update_slot_base: ke
} = window.__gradio__svelte__internal;
function ve(t) {
  let e, l, f;
  const i = (
    /*#slots*/
    t[18].default
  ), a = _e(
    i,
    t,
    /*$$scope*/
    t[17],
    null
  );
  let o = [
    { "data-testid": (
      /*test_id*/
      t[7]
    ) },
    { id: (
      /*elem_id*/
      t[2]
    ) },
    {
      class: l = "block " + /*elem_classes*/
      t[3].join(" ") + " svelte-1uxx6fq"
    }
  ], c = {};
  for (let n = 0; n < o.length; n += 1)
    c = se(c, o[n]);
  return {
    c() {
      e = re(
        /*tag*/
        t[14]
      ), a && a.c(), P(
        /*tag*/
        t[14]
      )(e, c), L(
        e,
        "hidden",
        /*visible*/
        t[10] === !1
      ), L(
        e,
        "padded",
        /*padding*/
        t[6]
      ), L(
        e,
        "border_focus",
        /*border_mode*/
        t[5] === "focus"
      ), L(e, "hide-container", !/*explicit_call*/
      t[8] && !/*container*/
      t[9]), y(
        e,
        "height",
        /*get_dimension*/
        t[15](
          /*height*/
          t[0]
        )
      ), y(e, "width", typeof /*width*/
      t[1] == "number" ? `calc(min(${/*width*/
      t[1]}px, 100%))` : (
        /*get_dimension*/
        t[15](
          /*width*/
          t[1]
        )
      )), y(
        e,
        "border-style",
        /*variant*/
        t[4]
      ), y(
        e,
        "overflow",
        /*allow_overflow*/
        t[11] ? "visible" : "hidden"
      ), y(
        e,
        "flex-grow",
        /*scale*/
        t[12]
      ), y(e, "min-width", `calc(min(${/*min_width*/
      t[13]}px, 100%))`), y(e, "border-width", "var(--block-border-width)");
    },
    m(n, s) {
      he(n, e, s), a && a.m(e, null), f = !0;
    },
    p(n, s) {
      a && a.p && (!f || s & /*$$scope*/
      131072) && ke(
        a,
        i,
        n,
        /*$$scope*/
        n[17],
        f ? me(
          i,
          /*$$scope*/
          n[17],
          s,
          null
        ) : ue(
          /*$$scope*/
          n[17]
        ),
        null
      ), P(
        /*tag*/
        n[14]
      )(e, c = be(o, [
        (!f || s & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          n[7]
        ) },
        (!f || s & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          n[2]
        ) },
        (!f || s & /*elem_classes*/
        8 && l !== (l = "block " + /*elem_classes*/
        n[3].join(" ") + " svelte-1uxx6fq")) && { class: l }
      ])), L(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), L(
        e,
        "padded",
        /*padding*/
        n[6]
      ), L(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), L(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), s & /*height*/
      1 && y(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), s & /*width*/
      2 && y(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), s & /*variant*/
      16 && y(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), s & /*allow_overflow*/
      2048 && y(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), s & /*scale*/
      4096 && y(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), s & /*min_width*/
      8192 && y(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`);
    },
    i(n) {
      f || (Z(a, n), f = !0);
    },
    o(n) {
      p(a, n), f = !1;
    },
    d(n) {
      n && de(e), a && a.d(n);
    }
  };
}
function ye(t) {
  let e, l = (
    /*tag*/
    t[14] && ve(t)
  );
  return {
    c() {
      l && l.c();
    },
    m(f, i) {
      l && l.m(f, i), e = !0;
    },
    p(f, [i]) {
      /*tag*/
      f[14] && l.p(f, i);
    },
    i(f) {
      e || (Z(l, f), e = !0);
    },
    o(f) {
      p(l, f), e = !1;
    },
    d(f) {
      l && l.d(f);
    }
  };
}
function ze(t, e, l) {
  let { $$slots: f = {}, $$scope: i } = e, { height: a = void 0 } = e, { width: o = void 0 } = e, { elem_id: c = "" } = e, { elem_classes: n = [] } = e, { variant: s = "solid" } = e, { border_mode: r = "base" } = e, { padding: m = !0 } = e, { type: u = "normal" } = e, { test_id: w = void 0 } = e, { explicit_call: j = !1 } = e, { container: z = !0 } = e, { visible: C = !0 } = e, { allow_overflow: q = !0 } = e, { scale: b = null } = e, { min_width: h = 0 } = e, I = u === "fieldset" ? "fieldset" : "div";
  const B = (d) => {
    if (d !== void 0) {
      if (typeof d == "number")
        return d + "px";
      if (typeof d == "string")
        return d;
    }
  };
  return t.$$set = (d) => {
    "height" in d && l(0, a = d.height), "width" in d && l(1, o = d.width), "elem_id" in d && l(2, c = d.elem_id), "elem_classes" in d && l(3, n = d.elem_classes), "variant" in d && l(4, s = d.variant), "border_mode" in d && l(5, r = d.border_mode), "padding" in d && l(6, m = d.padding), "type" in d && l(16, u = d.type), "test_id" in d && l(7, w = d.test_id), "explicit_call" in d && l(8, j = d.explicit_call), "container" in d && l(9, z = d.container), "visible" in d && l(10, C = d.visible), "allow_overflow" in d && l(11, q = d.allow_overflow), "scale" in d && l(12, b = d.scale), "min_width" in d && l(13, h = d.min_width), "$$scope" in d && l(17, i = d.$$scope);
  }, [
    a,
    o,
    c,
    n,
    s,
    r,
    m,
    w,
    j,
    z,
    C,
    q,
    b,
    h,
    I,
    B,
    u,
    i,
    f
  ];
}
class Ce extends ce {
  constructor(e) {
    super(), ge(this, e, ze, ye, we, {
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
const Se = [
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
], Q = {
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
Se.reduce(
  (t, { color: e, primary: l, secondary: f }) => ({
    ...t,
    [e]: {
      primary: Q[e][l],
      secondary: Q[e][f]
    }
  }),
  {}
);
const {
  SvelteComponent: je,
  attr: T,
  create_slot: qe,
  detach: Le,
  element: Me,
  get_all_dirty_from_scope: Ie,
  get_slot_changes: Be,
  init: Ee,
  insert: Ne,
  null_to_empty: R,
  safe_not_equal: He,
  set_style: Y,
  toggle_class: M,
  transition_in: Te,
  transition_out: Ye,
  update_slot_base: Ae
} = window.__gradio__svelte__internal;
function De(t) {
  let e, l, f = `calc(min(${/*min_width*/
  t[2]}px, 100%))`, i;
  const a = (
    /*#slots*/
    t[8].default
  ), o = qe(
    a,
    t,
    /*$$scope*/
    t[7],
    null
  );
  return {
    c() {
      e = Me("div"), o && o.c(), T(
        e,
        "id",
        /*elem_id*/
        t[3]
      ), T(e, "class", l = R(
        /*elem_classes*/
        t[4].join(" ")
      ) + " svelte-1m1obck"), M(
        e,
        "gap",
        /*gap*/
        t[1]
      ), M(
        e,
        "compact",
        /*variant*/
        t[6] === "compact"
      ), M(
        e,
        "panel",
        /*variant*/
        t[6] === "panel"
      ), M(e, "hide", !/*visible*/
      t[5]), Y(
        e,
        "flex-grow",
        /*scale*/
        t[0]
      ), Y(e, "min-width", f);
    },
    m(c, n) {
      Ne(c, e, n), o && o.m(e, null), i = !0;
    },
    p(c, [n]) {
      o && o.p && (!i || n & /*$$scope*/
      128) && Ae(
        o,
        a,
        c,
        /*$$scope*/
        c[7],
        i ? Be(
          a,
          /*$$scope*/
          c[7],
          n,
          null
        ) : Ie(
          /*$$scope*/
          c[7]
        ),
        null
      ), (!i || n & /*elem_id*/
      8) && T(
        e,
        "id",
        /*elem_id*/
        c[3]
      ), (!i || n & /*elem_classes*/
      16 && l !== (l = R(
        /*elem_classes*/
        c[4].join(" ")
      ) + " svelte-1m1obck")) && T(e, "class", l), (!i || n & /*elem_classes, gap*/
      18) && M(
        e,
        "gap",
        /*gap*/
        c[1]
      ), (!i || n & /*elem_classes, variant*/
      80) && M(
        e,
        "compact",
        /*variant*/
        c[6] === "compact"
      ), (!i || n & /*elem_classes, variant*/
      80) && M(
        e,
        "panel",
        /*variant*/
        c[6] === "panel"
      ), (!i || n & /*elem_classes, visible*/
      48) && M(e, "hide", !/*visible*/
      c[5]), n & /*scale*/
      1 && Y(
        e,
        "flex-grow",
        /*scale*/
        c[0]
      ), n & /*min_width*/
      4 && f !== (f = `calc(min(${/*min_width*/
      c[2]}px, 100%))`) && Y(e, "min-width", f);
    },
    i(c) {
      i || (Te(o, c), i = !0);
    },
    o(c) {
      Ye(o, c), i = !1;
    },
    d(c) {
      c && Le(e), o && o.d(c);
    }
  };
}
function Fe(t, e, l) {
  let { $$slots: f = {}, $$scope: i } = e, { scale: a = null } = e, { gap: o = !0 } = e, { min_width: c = 0 } = e, { elem_id: n = "" } = e, { elem_classes: s = [] } = e, { visible: r = !0 } = e, { variant: m = "default" } = e;
  return t.$$set = (u) => {
    "scale" in u && l(0, a = u.scale), "gap" in u && l(1, o = u.gap), "min_width" in u && l(2, c = u.min_width), "elem_id" in u && l(3, n = u.elem_id), "elem_classes" in u && l(4, s = u.elem_classes), "visible" in u && l(5, r = u.visible), "variant" in u && l(6, m = u.variant), "$$scope" in u && l(7, i = u.$$scope);
  }, [a, o, c, n, s, r, m, i, f];
}
let Ge = class extends je {
  constructor(e) {
    super(), Ee(this, e, Fe, De, He, {
      scale: 0,
      gap: 1,
      min_width: 2,
      elem_id: 3,
      elem_classes: 4,
      visible: 5,
      variant: 6
    });
  }
};
const {
  SvelteComponent: Je,
  append: k,
  attr: v,
  binding_callbacks: U,
  create_component: x,
  create_slot: Ke,
  destroy_component: $,
  detach: N,
  element: S,
  get_all_dirty_from_scope: Oe,
  get_slot_changes: Pe,
  init: Qe,
  insert: H,
  listen: A,
  mount_component: ee,
  noop: Re,
  run_all: Ue,
  safe_not_equal: Ve,
  set_data: F,
  set_style: g,
  space: E,
  text: G,
  toggle_class: V,
  transition_in: J,
  transition_out: K,
  update_slot_base: We
} = window.__gradio__svelte__internal;
function W(t) {
  let e, l, f;
  return {
    c() {
      e = S("div"), e.innerHTML = '<svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 1L9 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M9 1L1 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>', v(e, "class", "close svelte-sz1hib");
    },
    m(i, a) {
      H(i, e, a), l || (f = A(
        e,
        "click",
        /*close*/
        t[13]
      ), l = !0);
    },
    p: Re,
    d(i) {
      i && N(e), l = !1, f();
    }
  };
}
function Xe(t) {
  let e;
  const l = (
    /*#slots*/
    t[22].default
  ), f = Ke(
    l,
    t,
    /*$$scope*/
    t[26],
    null
  );
  return {
    c() {
      f && f.c();
    },
    m(i, a) {
      f && f.m(i, a), e = !0;
    },
    p(i, a) {
      f && f.p && (!e || a & /*$$scope*/
      67108864) && We(
        f,
        l,
        i,
        /*$$scope*/
        i[26],
        e ? Pe(
          l,
          /*$$scope*/
          i[26],
          a,
          null
        ) : Oe(
          /*$$scope*/
          i[26]
        ),
        null
      );
    },
    i(i) {
      e || (J(f, i), e = !0);
    },
    o(i) {
      K(f, i), e = !1;
    },
    d(i) {
      f && f.d(i);
    }
  };
}
function Ze(t) {
  let e, l, f, i, a = (
    /*display_close_icon*/
    t[3] && W(t)
  );
  return f = new Ge({
    props: {
      elem_classes: ["centered-column"],
      $$slots: { default: [Xe] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      a && a.c(), e = E(), l = S("div"), x(f.$$.fragment), v(l, "class", "modal-content svelte-sz1hib"), v(
        l,
        "style",
        /*getSizeStyle*/
        t[16]()
      );
    },
    m(o, c) {
      a && a.m(o, c), H(o, e, c), H(o, l, c), ee(f, l, null), i = !0;
    },
    p(o, c) {
      /*display_close_icon*/
      o[3] ? a ? a.p(o, c) : (a = W(o), a.c(), a.m(e.parentNode, e)) : a && (a.d(1), a = null);
      const n = {};
      c & /*$$scope*/
      67108864 && (n.$$scope = { dirty: c, ctx: o }), f.$set(n);
    },
    i(o) {
      i || (J(f.$$.fragment, o), i = !0);
    },
    o(o) {
      K(f.$$.fragment, o), i = !1;
    },
    d(o) {
      o && (N(e), N(l)), a && a.d(o), $(f);
    }
  };
}
function X(t) {
  let e, l, f, i, a, o, c, n, s, r = (
    /*close_message_style*/
    t[9].confirm_text + ""
  ), m, u, w, j = (
    /*close_message_style*/
    t[9].cancel_text + ""
  ), z, C, q;
  return {
    c() {
      e = S("div"), l = S("div"), f = S("h3"), i = G(
        /*close_message*/
        t[5]
      ), a = E(), o = S("br"), c = E(), n = S("div"), s = S("button"), m = G(r), u = E(), w = S("button"), z = G(j), g(
        f,
        "color",
        /*close_message_style*/
        t[9].message_color
      ), v(f, "class", "svelte-sz1hib"), v(s, "class", "yes-button svelte-sz1hib"), g(
        s,
        "background-color",
        /*close_message_style*/
        t[9].confirm_bg_color
      ), g(
        s,
        "color",
        /*close_message_style*/
        t[9].confirm_text_color
      ), v(w, "class", "no-button svelte-sz1hib"), g(
        w,
        "background-color",
        /*close_message_style*/
        t[9].cancel_bg_color
      ), g(
        w,
        "color",
        /*close_message_style*/
        t[9].cancel_text_color
      ), v(n, "class", "confirmation-buttons svelte-sz1hib"), v(l, "class", "confirmation-content svelte-sz1hib"), g(
        l,
        "background-color",
        /*close_message_style*/
        t[9].modal_bg_color
      ), v(e, "class", "confirmation-modal svelte-sz1hib");
    },
    m(b, h) {
      H(b, e, h), k(e, l), k(l, f), k(f, i), k(l, a), k(l, o), k(l, c), k(l, n), k(n, s), k(s, m), k(n, u), k(n, w), k(w, z), C || (q = [
        A(
          s,
          "click",
          /*closeModal*/
          t[14]
        ),
        A(
          w,
          "click",
          /*cancelClose*/
          t[15]
        )
      ], C = !0);
    },
    p(b, h) {
      h & /*close_message*/
      32 && F(
        i,
        /*close_message*/
        b[5]
      ), h & /*close_message_style*/
      512 && g(
        f,
        "color",
        /*close_message_style*/
        b[9].message_color
      ), h & /*close_message_style*/
      512 && r !== (r = /*close_message_style*/
      b[9].confirm_text + "") && F(m, r), h & /*close_message_style*/
      512 && g(
        s,
        "background-color",
        /*close_message_style*/
        b[9].confirm_bg_color
      ), h & /*close_message_style*/
      512 && g(
        s,
        "color",
        /*close_message_style*/
        b[9].confirm_text_color
      ), h & /*close_message_style*/
      512 && j !== (j = /*close_message_style*/
      b[9].cancel_text + "") && F(z, j), h & /*close_message_style*/
      512 && g(
        w,
        "background-color",
        /*close_message_style*/
        b[9].cancel_bg_color
      ), h & /*close_message_style*/
      512 && g(
        w,
        "color",
        /*close_message_style*/
        b[9].cancel_text_color
      ), h & /*close_message_style*/
      512 && g(
        l,
        "background-color",
        /*close_message_style*/
        b[9].modal_bg_color
      );
    },
    d(b) {
      b && N(e), C = !1, Ue(q);
    }
  };
}
function pe(t) {
  let e, l, f, i, a, o, c, n;
  f = new Ce({
    props: {
      allow_overflow: !1,
      elem_classes: ["modal-block"],
      $$slots: { default: [Ze] },
      $$scope: { ctx: t }
    }
  });
  let s = (
    /*showConfirmation*/
    t[12] && X(t)
  );
  return {
    c() {
      e = S("div"), l = S("div"), x(f.$$.fragment), i = E(), s && s.c(), v(l, "class", "modal-container svelte-sz1hib"), g(
        l,
        "width",
        /*width*/
        t[7] + "px"
      ), g(
        l,
        "height",
        /*height*/
        t[8] + "px"
      ), v(e, "class", a = "modal " + /*elem_classes*/
      t[2].join(" ") + " svelte-sz1hib"), v(
        e,
        "id",
        /*elem_id*/
        t[1]
      ), g(e, "backdrop-filter", "blur(" + /*bg_blur*/
      t[6] + ")"), V(e, "hide", !/*visible*/
      t[0]);
    },
    m(r, m) {
      H(r, e, m), k(e, l), ee(f, l, null), t[23](l), k(e, i), s && s.m(e, null), t[24](e), o = !0, c || (n = A(
        e,
        "click",
        /*click_handler*/
        t[25]
      ), c = !0);
    },
    p(r, [m]) {
      const u = {};
      m & /*$$scope, display_close_icon*/
      67108872 && (u.$$scope = { dirty: m, ctx: r }), f.$set(u), (!o || m & /*width*/
      128) && g(
        l,
        "width",
        /*width*/
        r[7] + "px"
      ), (!o || m & /*height*/
      256) && g(
        l,
        "height",
        /*height*/
        r[8] + "px"
      ), /*showConfirmation*/
      r[12] ? s ? s.p(r, m) : (s = X(r), s.c(), s.m(e, null)) : s && (s.d(1), s = null), (!o || m & /*elem_classes*/
      4 && a !== (a = "modal " + /*elem_classes*/
      r[2].join(" ") + " svelte-sz1hib")) && v(e, "class", a), (!o || m & /*elem_id*/
      2) && v(
        e,
        "id",
        /*elem_id*/
        r[1]
      ), (!o || m & /*bg_blur*/
      64) && g(e, "backdrop-filter", "blur(" + /*bg_blur*/
      r[6] + ")"), (!o || m & /*elem_classes, visible*/
      5) && V(e, "hide", !/*visible*/
      r[0]);
    },
    i(r) {
      o || (J(f.$$.fragment, r), o = !0);
    },
    o(r) {
      K(f.$$.fragment, r), o = !1;
    },
    d(r) {
      r && N(e), $(f), t[23](null), s && s.d(), t[24](null), c = !1, n();
    }
  };
}
function xe(t, e, l) {
  let { $$slots: f = {}, $$scope: i } = e, { elem_id: a = "" } = e, { elem_classes: o = [] } = e, { visible: c = !1 } = e, { display_close_icon: n = !1 } = e, { close_on_esc: s } = e, { close_outer_click: r } = e, { close_message: m } = e, { bg_blur: u } = e, { width: w } = e, { height: j } = e, { content_width_percent: z } = e, { content_height_percent: C } = e, { content_padding: q } = e, { gradio: b } = e, { close_message_style: h = {
    message_color: "var(--body-text-color)",
    confirm_text: "Yes",
    cancel_text: "No",
    confirm_bg_color: "var(--primary-500)",
    cancel_bg_color: "var(--neutral-500)",
    confirm_text_color: "white",
    cancel_text_color: "white",
    modal_bg_color: "var(--background-fill-primary)"
  } } = e, I = null, B = null, d = !1;
  const D = () => {
    m ? l(12, d = !0) : O();
  }, O = () => {
    l(0, c = !1), l(12, d = !1), b.dispatch("blur");
  }, le = () => {
    l(12, d = !1);
  };
  document.addEventListener("keydown", (_) => {
    s && _.key === "Escape" && D();
  });
  const te = () => {
    const _ = q ? `${q}` : "0px", ae = z ? `${z}%` : "100%", oe = C ? `${C}%` : "100%";
    return `width: ${ae}; max-height: ${oe}; padding: ${_};`;
  };
  function fe(_) {
    U[_ ? "unshift" : "push"](() => {
      B = _, l(11, B);
    });
  }
  function ne(_) {
    U[_ ? "unshift" : "push"](() => {
      I = _, l(10, I);
    });
  }
  const ie = (_) => {
    r && (_.target === I || _.target === B) && D();
  };
  return t.$$set = (_) => {
    "elem_id" in _ && l(1, a = _.elem_id), "elem_classes" in _ && l(2, o = _.elem_classes), "visible" in _ && l(0, c = _.visible), "display_close_icon" in _ && l(3, n = _.display_close_icon), "close_on_esc" in _ && l(17, s = _.close_on_esc), "close_outer_click" in _ && l(4, r = _.close_outer_click), "close_message" in _ && l(5, m = _.close_message), "bg_blur" in _ && l(6, u = _.bg_blur), "width" in _ && l(7, w = _.width), "height" in _ && l(8, j = _.height), "content_width_percent" in _ && l(18, z = _.content_width_percent), "content_height_percent" in _ && l(19, C = _.content_height_percent), "content_padding" in _ && l(20, q = _.content_padding), "gradio" in _ && l(21, b = _.gradio), "close_message_style" in _ && l(9, h = _.close_message_style), "$$scope" in _ && l(26, i = _.$$scope);
  }, [
    c,
    a,
    o,
    n,
    r,
    m,
    u,
    w,
    j,
    h,
    I,
    B,
    d,
    D,
    O,
    le,
    te,
    s,
    z,
    C,
    q,
    b,
    f,
    fe,
    ne,
    ie,
    i
  ];
}
class e0 extends Je {
  constructor(e) {
    super(), Qe(this, e, xe, pe, Ve, {
      elem_id: 1,
      elem_classes: 2,
      visible: 0,
      display_close_icon: 3,
      close_on_esc: 17,
      close_outer_click: 4,
      close_message: 5,
      bg_blur: 6,
      width: 7,
      height: 8,
      content_width_percent: 18,
      content_height_percent: 19,
      content_padding: 20,
      gradio: 21,
      close_message_style: 9
    });
  }
}
export {
  e0 as default
};
