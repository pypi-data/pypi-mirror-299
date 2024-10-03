const {
  SvelteComponent: $,
  assign: ee,
  create_slot: le,
  detach: te,
  element: fe,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ne,
  get_spread_update: ae,
  init: se,
  insert: ce,
  safe_not_equal: oe,
  set_dynamic_element_data: G,
  set_style: b,
  toggle_class: C,
  transition_in: U,
  transition_out: V,
  update_slot_base: de
} = window.__gradio__svelte__internal;
function _e(t) {
  let e, l, i;
  const n = (
    /*#slots*/
    t[18].default
  ), a = le(
    n,
    t,
    /*$$scope*/
    t[17],
    null
  );
  let s = [
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
      t[3].join(" ") + " svelte-1t38q2d"
    }
  ], c = {};
  for (let f = 0; f < s.length; f += 1)
    c = ee(c, s[f]);
  return {
    c() {
      e = fe(
        /*tag*/
        t[14]
      ), a && a.c(), G(
        /*tag*/
        t[14]
      )(e, c), C(
        e,
        "hidden",
        /*visible*/
        t[10] === !1
      ), C(
        e,
        "padded",
        /*padding*/
        t[6]
      ), C(
        e,
        "border_focus",
        /*border_mode*/
        t[5] === "focus"
      ), C(e, "hide-container", !/*explicit_call*/
      t[8] && !/*container*/
      t[9]), b(
        e,
        "height",
        /*get_dimension*/
        t[15](
          /*height*/
          t[0]
        )
      ), b(e, "width", typeof /*width*/
      t[1] == "number" ? `calc(min(${/*width*/
      t[1]}px, 100%))` : (
        /*get_dimension*/
        t[15](
          /*width*/
          t[1]
        )
      )), b(
        e,
        "border-style",
        /*variant*/
        t[4]
      ), b(
        e,
        "overflow",
        /*allow_overflow*/
        t[11] ? "visible" : "hidden"
      ), b(
        e,
        "flex-grow",
        /*scale*/
        t[12]
      ), b(e, "min-width", `calc(min(${/*min_width*/
      t[13]}px, 100%))`), b(e, "border-width", "var(--block-border-width)");
    },
    m(f, o) {
      ce(f, e, o), a && a.m(e, null), i = !0;
    },
    p(f, o) {
      a && a.p && (!i || o & /*$$scope*/
      131072) && de(
        a,
        n,
        f,
        /*$$scope*/
        f[17],
        i ? ne(
          n,
          /*$$scope*/
          f[17],
          o,
          null
        ) : ie(
          /*$$scope*/
          f[17]
        ),
        null
      ), G(
        /*tag*/
        f[14]
      )(e, c = ae(s, [
        (!i || o & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          f[7]
        ) },
        (!i || o & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          f[2]
        ) },
        (!i || o & /*elem_classes*/
        8 && l !== (l = "block " + /*elem_classes*/
        f[3].join(" ") + " svelte-1t38q2d")) && { class: l }
      ])), C(
        e,
        "hidden",
        /*visible*/
        f[10] === !1
      ), C(
        e,
        "padded",
        /*padding*/
        f[6]
      ), C(
        e,
        "border_focus",
        /*border_mode*/
        f[5] === "focus"
      ), C(e, "hide-container", !/*explicit_call*/
      f[8] && !/*container*/
      f[9]), o & /*height*/
      1 && b(
        e,
        "height",
        /*get_dimension*/
        f[15](
          /*height*/
          f[0]
        )
      ), o & /*width*/
      2 && b(e, "width", typeof /*width*/
      f[1] == "number" ? `calc(min(${/*width*/
      f[1]}px, 100%))` : (
        /*get_dimension*/
        f[15](
          /*width*/
          f[1]
        )
      )), o & /*variant*/
      16 && b(
        e,
        "border-style",
        /*variant*/
        f[4]
      ), o & /*allow_overflow*/
      2048 && b(
        e,
        "overflow",
        /*allow_overflow*/
        f[11] ? "visible" : "hidden"
      ), o & /*scale*/
      4096 && b(
        e,
        "flex-grow",
        /*scale*/
        f[12]
      ), o & /*min_width*/
      8192 && b(e, "min-width", `calc(min(${/*min_width*/
      f[13]}px, 100%))`);
    },
    i(f) {
      i || (U(a, f), i = !0);
    },
    o(f) {
      V(a, f), i = !1;
    },
    d(f) {
      f && te(e), a && a.d(f);
    }
  };
}
function re(t) {
  let e, l = (
    /*tag*/
    t[14] && _e(t)
  );
  return {
    c() {
      l && l.c();
    },
    m(i, n) {
      l && l.m(i, n), e = !0;
    },
    p(i, [n]) {
      /*tag*/
      i[14] && l.p(i, n);
    },
    i(i) {
      e || (U(l, i), e = !0);
    },
    o(i) {
      V(l, i), e = !1;
    },
    d(i) {
      l && l.d(i);
    }
  };
}
function ue(t, e, l) {
  let { $$slots: i = {}, $$scope: n } = e, { height: a = void 0 } = e, { width: s = void 0 } = e, { elem_id: c = "" } = e, { elem_classes: f = [] } = e, { variant: o = "solid" } = e, { border_mode: r = "base" } = e, { padding: m = !0 } = e, { type: u = "normal" } = e, { test_id: y = void 0 } = e, { explicit_call: w = !1 } = e, { container: k = !0 } = e, { visible: q = !0 } = e, { allow_overflow: S = !0 } = e, { scale: L = null } = e, { min_width: M = 0 } = e, z = u === "fieldset" ? "fieldset" : "div";
  const A = (d) => {
    if (d !== void 0) {
      if (typeof d == "number")
        return d + "px";
      if (typeof d == "string")
        return d;
    }
  };
  return t.$$set = (d) => {
    "height" in d && l(0, a = d.height), "width" in d && l(1, s = d.width), "elem_id" in d && l(2, c = d.elem_id), "elem_classes" in d && l(3, f = d.elem_classes), "variant" in d && l(4, o = d.variant), "border_mode" in d && l(5, r = d.border_mode), "padding" in d && l(6, m = d.padding), "type" in d && l(16, u = d.type), "test_id" in d && l(7, y = d.test_id), "explicit_call" in d && l(8, w = d.explicit_call), "container" in d && l(9, k = d.container), "visible" in d && l(10, q = d.visible), "allow_overflow" in d && l(11, S = d.allow_overflow), "scale" in d && l(12, L = d.scale), "min_width" in d && l(13, M = d.min_width), "$$scope" in d && l(17, n = d.$$scope);
  }, [
    a,
    s,
    c,
    f,
    o,
    r,
    m,
    y,
    w,
    k,
    q,
    S,
    L,
    M,
    z,
    A,
    u,
    n,
    i
  ];
}
class me extends $ {
  constructor(e) {
    super(), se(this, e, ue, re, oe, {
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
const be = [
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
], J = {
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
be.reduce(
  (t, { color: e, primary: l, secondary: i }) => ({
    ...t,
    [e]: {
      primary: J[e][l],
      secondary: J[e][i]
    }
  }),
  {}
);
const {
  SvelteComponent: he,
  attr: H,
  create_slot: ge,
  detach: we,
  element: ve,
  get_all_dirty_from_scope: ke,
  get_slot_changes: ye,
  init: Ce,
  insert: je,
  null_to_empty: K,
  safe_not_equal: qe,
  set_style: T,
  toggle_class: j,
  transition_in: Se,
  transition_out: Le,
  update_slot_base: Me
} = window.__gradio__svelte__internal;
function Ie(t) {
  let e, l, i = `calc(min(${/*min_width*/
  t[2]}px, 100%))`, n;
  const a = (
    /*#slots*/
    t[8].default
  ), s = ge(
    a,
    t,
    /*$$scope*/
    t[7],
    null
  );
  return {
    c() {
      e = ve("div"), s && s.c(), H(
        e,
        "id",
        /*elem_id*/
        t[3]
      ), H(e, "class", l = K(
        /*elem_classes*/
        t[4].join(" ")
      ) + " svelte-1m1obck"), j(
        e,
        "gap",
        /*gap*/
        t[1]
      ), j(
        e,
        "compact",
        /*variant*/
        t[6] === "compact"
      ), j(
        e,
        "panel",
        /*variant*/
        t[6] === "panel"
      ), j(e, "hide", !/*visible*/
      t[5]), T(
        e,
        "flex-grow",
        /*scale*/
        t[0]
      ), T(e, "min-width", i);
    },
    m(c, f) {
      je(c, e, f), s && s.m(e, null), n = !0;
    },
    p(c, [f]) {
      s && s.p && (!n || f & /*$$scope*/
      128) && Me(
        s,
        a,
        c,
        /*$$scope*/
        c[7],
        n ? ye(
          a,
          /*$$scope*/
          c[7],
          f,
          null
        ) : ke(
          /*$$scope*/
          c[7]
        ),
        null
      ), (!n || f & /*elem_id*/
      8) && H(
        e,
        "id",
        /*elem_id*/
        c[3]
      ), (!n || f & /*elem_classes*/
      16 && l !== (l = K(
        /*elem_classes*/
        c[4].join(" ")
      ) + " svelte-1m1obck")) && H(e, "class", l), (!n || f & /*elem_classes, gap*/
      18) && j(
        e,
        "gap",
        /*gap*/
        c[1]
      ), (!n || f & /*elem_classes, variant*/
      80) && j(
        e,
        "compact",
        /*variant*/
        c[6] === "compact"
      ), (!n || f & /*elem_classes, variant*/
      80) && j(
        e,
        "panel",
        /*variant*/
        c[6] === "panel"
      ), (!n || f & /*elem_classes, visible*/
      48) && j(e, "hide", !/*visible*/
      c[5]), f & /*scale*/
      1 && T(
        e,
        "flex-grow",
        /*scale*/
        c[0]
      ), f & /*min_width*/
      4 && i !== (i = `calc(min(${/*min_width*/
      c[2]}px, 100%))`) && T(e, "min-width", i);
    },
    i(c) {
      n || (Se(s, c), n = !0);
    },
    o(c) {
      Le(s, c), n = !1;
    },
    d(c) {
      c && we(e), s && s.d(c);
    }
  };
}
function Be(t, e, l) {
  let { $$slots: i = {}, $$scope: n } = e, { scale: a = null } = e, { gap: s = !0 } = e, { min_width: c = 0 } = e, { elem_id: f = "" } = e, { elem_classes: o = [] } = e, { visible: r = !0 } = e, { variant: m = "default" } = e;
  return t.$$set = (u) => {
    "scale" in u && l(0, a = u.scale), "gap" in u && l(1, s = u.gap), "min_width" in u && l(2, c = u.min_width), "elem_id" in u && l(3, f = u.elem_id), "elem_classes" in u && l(4, o = u.elem_classes), "visible" in u && l(5, r = u.visible), "variant" in u && l(6, m = u.variant), "$$scope" in u && l(7, n = u.$$scope);
  }, [a, s, c, f, o, r, m, n, i];
}
let Ee = class extends he {
  constructor(e) {
    super(), Ce(this, e, Be, Ie, qe, {
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
  SvelteComponent: Ne,
  append: g,
  attr: h,
  binding_callbacks: O,
  create_component: W,
  create_slot: ze,
  destroy_component: X,
  detach: E,
  element: v,
  get_all_dirty_from_scope: He,
  get_slot_changes: Te,
  init: Ye,
  insert: N,
  listen: Y,
  mount_component: Z,
  noop: Ae,
  run_all: De,
  safe_not_equal: Fe,
  set_data: Ge,
  set_style: I,
  space: B,
  text: Je,
  toggle_class: P,
  transition_in: D,
  transition_out: F,
  update_slot_base: Ke
} = window.__gradio__svelte__internal;
function Q(t) {
  let e, l, i;
  return {
    c() {
      e = v("div"), e.innerHTML = '<svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 1L9 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M9 1L1 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>', h(e, "class", "close svelte-114irsb");
    },
    m(n, a) {
      N(n, e, a), l || (i = Y(
        e,
        "click",
        /*close*/
        t[12]
      ), l = !0);
    },
    p: Ae,
    d(n) {
      n && E(e), l = !1, i();
    }
  };
}
function Oe(t) {
  let e;
  const l = (
    /*#slots*/
    t[17].default
  ), i = ze(
    l,
    t,
    /*$$scope*/
    t[21],
    null
  );
  return {
    c() {
      i && i.c();
    },
    m(n, a) {
      i && i.m(n, a), e = !0;
    },
    p(n, a) {
      i && i.p && (!e || a & /*$$scope*/
      2097152) && Ke(
        i,
        l,
        n,
        /*$$scope*/
        n[21],
        e ? Te(
          l,
          /*$$scope*/
          n[21],
          a,
          null
        ) : He(
          /*$$scope*/
          n[21]
        ),
        null
      );
    },
    i(n) {
      e || (D(i, n), e = !0);
    },
    o(n) {
      F(i, n), e = !1;
    },
    d(n) {
      i && i.d(n);
    }
  };
}
function Pe(t) {
  let e, l, i, n, a = (
    /*allow_user_close*/
    t[3] && Q(t)
  );
  return i = new Ee({
    props: {
      elem_classes: ["centered-column"],
      $$slots: { default: [Oe] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      a && a.c(), e = B(), l = v("div"), W(i.$$.fragment), h(l, "class", "modal-content svelte-114irsb");
    },
    m(s, c) {
      a && a.m(s, c), N(s, e, c), N(s, l, c), Z(i, l, null), n = !0;
    },
    p(s, c) {
      /*allow_user_close*/
      s[3] ? a ? a.p(s, c) : (a = Q(s), a.c(), a.m(e.parentNode, e)) : a && (a.d(1), a = null);
      const f = {};
      c & /*$$scope*/
      2097152 && (f.$$scope = { dirty: c, ctx: s }), i.$set(f);
    },
    i(s) {
      n || (D(i.$$.fragment, s), n = !0);
    },
    o(s) {
      F(i.$$.fragment, s), n = !1;
    },
    d(s) {
      s && (E(e), E(l)), a && a.d(s), X(i);
    }
  };
}
function R(t) {
  let e, l, i, n, a, s, c, f, o, r, m, u, y;
  return {
    c() {
      e = v("div"), l = v("div"), i = v("h3"), n = Je(
        /*close_message*/
        t[5]
      ), a = B(), s = v("br"), c = B(), f = v("div"), o = v("button"), o.textContent = "Yes", r = B(), m = v("button"), m.textContent = "No", h(i, "class", "svelte-114irsb"), h(o, "class", "yes-button svelte-114irsb"), h(m, "class", "no-button svelte-114irsb"), h(f, "class", "confirmation-buttons svelte-114irsb"), h(l, "class", "confirmation-content svelte-114irsb"), h(e, "class", "confirmation-modal svelte-114irsb");
    },
    m(w, k) {
      N(w, e, k), g(e, l), g(l, i), g(i, n), g(l, a), g(l, s), g(l, c), g(l, f), g(f, o), g(f, r), g(f, m), u || (y = [
        Y(
          o,
          "click",
          /*closeModal*/
          t[13]
        ),
        Y(
          m,
          "click",
          /*cancelClose*/
          t[14]
        )
      ], u = !0);
    },
    p(w, k) {
      k & /*close_message*/
      32 && Ge(
        n,
        /*close_message*/
        w[5]
      );
    },
    d(w) {
      w && E(e), u = !1, De(y);
    }
  };
}
function Qe(t) {
  let e, l, i, n, a, s, c, f;
  i = new me({
    props: {
      allow_overflow: !1,
      elem_classes: ["modal-block"],
      $$slots: { default: [Pe] },
      $$scope: { ctx: t }
    }
  });
  let o = (
    /*showConfirmation*/
    t[11] && R(t)
  );
  return {
    c() {
      e = v("div"), l = v("div"), W(i.$$.fragment), n = B(), o && o.c(), h(l, "class", "modal-container svelte-114irsb"), I(
        l,
        "width",
        /*width*/
        t[7] + "px"
      ), I(
        l,
        "height",
        /*height*/
        t[8] + "px"
      ), h(e, "class", a = "modal " + /*elem_classes*/
      t[2].join(" ") + " svelte-114irsb"), h(
        e,
        "id",
        /*elem_id*/
        t[1]
      ), I(e, "backdrop-filter", "blur(" + /*bg_blur*/
      t[6] + ")"), P(e, "hide", !/*visible*/
      t[0]);
    },
    m(r, m) {
      N(r, e, m), g(e, l), Z(i, l, null), t[18](l), g(e, n), o && o.m(e, null), t[19](e), s = !0, c || (f = Y(
        e,
        "click",
        /*click_handler*/
        t[20]
      ), c = !0);
    },
    p(r, [m]) {
      const u = {};
      m & /*$$scope, allow_user_close*/
      2097160 && (u.$$scope = { dirty: m, ctx: r }), i.$set(u), (!s || m & /*width*/
      128) && I(
        l,
        "width",
        /*width*/
        r[7] + "px"
      ), (!s || m & /*height*/
      256) && I(
        l,
        "height",
        /*height*/
        r[8] + "px"
      ), /*showConfirmation*/
      r[11] ? o ? o.p(r, m) : (o = R(r), o.c(), o.m(e, null)) : o && (o.d(1), o = null), (!s || m & /*elem_classes*/
      4 && a !== (a = "modal " + /*elem_classes*/
      r[2].join(" ") + " svelte-114irsb")) && h(e, "class", a), (!s || m & /*elem_id*/
      2) && h(
        e,
        "id",
        /*elem_id*/
        r[1]
      ), (!s || m & /*bg_blur*/
      64) && I(e, "backdrop-filter", "blur(" + /*bg_blur*/
      r[6] + ")"), (!s || m & /*elem_classes, visible*/
      5) && P(e, "hide", !/*visible*/
      r[0]);
    },
    i(r) {
      s || (D(i.$$.fragment, r), s = !0);
    },
    o(r) {
      F(i.$$.fragment, r), s = !1;
    },
    d(r) {
      r && E(e), X(i), t[18](null), o && o.d(), t[19](null), c = !1, f();
    }
  };
}
function Re(t, e, l) {
  let { $$slots: i = {}, $$scope: n } = e, { elem_id: a = "" } = e, { elem_classes: s = [] } = e, { visible: c = !1 } = e, { allow_user_close: f = !1 } = e, { close_on_esc: o } = e, { close_outer_click: r } = e, { close_message: m } = e, { bg_blur: u } = e, { width: y } = e, { height: w } = e, { gradio: k } = e, q = null, S = null, L = !1;
  const M = () => {
    m ? l(11, L = !0) : z();
  }, z = () => {
    l(0, c = !1), l(11, L = !1), k.dispatch("blur");
  }, A = () => {
    l(11, L = !1);
  };
  document.addEventListener("keydown", (_) => {
    o && _.key === "Escape" && M();
  });
  function d(_) {
    O[_ ? "unshift" : "push"](() => {
      S = _, l(10, S);
    });
  }
  function p(_) {
    O[_ ? "unshift" : "push"](() => {
      q = _, l(9, q);
    });
  }
  const x = (_) => {
    r && (_.target === q || _.target === S) && M();
  };
  return t.$$set = (_) => {
    "elem_id" in _ && l(1, a = _.elem_id), "elem_classes" in _ && l(2, s = _.elem_classes), "visible" in _ && l(0, c = _.visible), "allow_user_close" in _ && l(3, f = _.allow_user_close), "close_on_esc" in _ && l(15, o = _.close_on_esc), "close_outer_click" in _ && l(4, r = _.close_outer_click), "close_message" in _ && l(5, m = _.close_message), "bg_blur" in _ && l(6, u = _.bg_blur), "width" in _ && l(7, y = _.width), "height" in _ && l(8, w = _.height), "gradio" in _ && l(16, k = _.gradio), "$$scope" in _ && l(21, n = _.$$scope);
  }, [
    c,
    a,
    s,
    f,
    r,
    m,
    u,
    y,
    w,
    q,
    S,
    L,
    M,
    z,
    A,
    o,
    k,
    i,
    d,
    p,
    x,
    n
  ];
}
class Ve extends Ne {
  constructor(e) {
    super(), Ye(this, e, Re, Qe, Fe, {
      elem_id: 1,
      elem_classes: 2,
      visible: 0,
      allow_user_close: 3,
      close_on_esc: 15,
      close_outer_click: 4,
      close_message: 5,
      bg_blur: 6,
      width: 7,
      height: 8,
      gradio: 16
    });
  }
}
export {
  Ve as default
};
