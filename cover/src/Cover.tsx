import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont("normal", { weights: ["400", "500", "600", "700", "800"] });

const C = { bg: "#F4F5F7", ink: "#0F1115", muted: "#5B6170", line: "#E3E6EB", blue: "#2F6BFF", violet: "#7C4DFF", green: "#14955B" };

const STACK = ["Python", "OpenAI API", "Claude Code", "Cloudflare Workers", "Cloudflare D1", "Gmail", "FMCSA Open Data"];

const POINTS = [
  { title: "Finds & qualifies leads", sub: "Registry data + AI reads every website" },
  { title: "Writes personal emails", sub: "One real fact per company, human-approved" },
  { title: "Follows up & predicts deals", sub: "Reads replies, scores who will buy" },
];

const Check: React.FC<{ color: string }> = ({ color }) => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
    <circle cx="12" cy="12" r="12" fill={color} opacity="0.12" />
    <path d="M7 12.5l3.2 3.2L17 9" stroke={color} strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const Browser: React.FC<{ width: number; src: string; ratio: number }> = ({ width, src, ratio }) => (
  <div style={{ width, borderRadius: 22, background: "#fff", border: `1px solid ${C.line}`, overflow: "hidden",
    boxShadow: "0 40px 80px -20px rgba(15,17,21,0.28), 0 12px 24px -12px rgba(15,17,21,0.18)" }}>
    <div style={{ height: 40, display: "flex", alignItems: "center", gap: 8, padding: "0 16px", borderBottom: `1px solid ${C.line}`, background: "#FAFBFC" }}>
      {["#FF5F57", "#FEBC2E", "#28C840"].map((c) => <span key={c} style={{ width: 12, height: 12, borderRadius: 6, background: c }} />)}
      <div style={{ marginLeft: 16, flex: 1, height: 22, borderRadius: 11, background: "#EEF0F3", maxWidth: 360 }} />
    </div>
    <Img src={staticFile(src)} style={{ width, height: width * ratio, display: "block", objectFit: "cover", objectPosition: "top" }} />
  </div>
);

export const Cover: React.FC<{ wide: boolean }> = ({ wide }) => {
  const pad = wide ? 88 : 84;
  return (
    <AbsoluteFill style={{ background: C.bg, fontFamily, color: C.ink, overflow: "hidden" }}>
      {/* soft brand glow + dot grid */}
      <div style={{ position: "absolute", width: 1100, height: 1100, borderRadius: "50%", right: -380, top: -420,
        background: `radial-gradient(circle, ${C.blue}2E 0%, ${C.violet}14 40%, transparent 70%)` }} />
      <div style={{ position: "absolute", inset: 0, backgroundImage: "radial-gradient(#0F111514 1.2px, transparent 1.2px)", backgroundSize: "28px 28px",
        maskImage: "linear-gradient(180deg, black 0%, transparent 70%)", WebkitMaskImage: "linear-gradient(180deg, black 0%, transparent 70%)" }} />

      {/* text column */}
      <div style={{ position: "absolute", left: pad, top: pad - 4, width: wide ? 820 : 1600 - pad * 2 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <Img src={staticFile("logo.png")} style={{ width: 48, height: 48, borderRadius: 12 }} />
          <span style={{ fontSize: 24, fontWeight: 700, letterSpacing: -0.3 }}>WeBoost Sales Engine</span>
          <span style={{ marginLeft: 10, fontSize: 16, fontWeight: 600, color: C.blue, background: "#E8EFFF", padding: "7px 14px", borderRadius: 99 }}>
            Agentic AI automation
          </span>
        </div>

        <div style={{ fontSize: wide ? 66 : 82, fontWeight: 800, lineHeight: 1.02, letterSpacing: -3, marginTop: wide ? 56 : 52 }}>
          Your next clients,<br />
          <span style={{ background: `linear-gradient(90deg, ${C.blue}, ${C.violet})`, WebkitBackgroundClip: "text", color: "transparent" }}>
            found and emailed by AI.
          </span>
        </div>
        <div style={{ fontSize: wide ? 25 : 27, lineHeight: 1.45, color: C.muted, marginTop: 26, maxWidth: wide ? 760 : 1180 }}>
          An outbound engine that researches every company, writes a personal email, follows up, reads the replies and tells you who is ready to buy.
        </div>

        <div style={{ display: "flex", flexDirection: wide ? "column" : "row", gap: wide ? 22 : 34, marginTop: wide ? 40 : 38 }}>
          {POINTS.map((p, i) => (
            <div key={p.title} style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
              <div style={{ marginTop: 3 }}><Check color={[C.blue, C.violet, C.green][i]} /></div>
              <div>
                <div style={{ fontSize: 21, fontWeight: 700 }}>{p.title}</div>
                <div style={{ fontSize: 17, color: C.muted, marginTop: 4 }}>{p.sub}</div>
              </div>
            </div>
          ))}
        </div>

        <div style={{ marginTop: wide ? 44 : 40, display: "flex", flexWrap: "wrap", gap: 10, alignItems: "center" }}>
          <span style={{ fontSize: 15, fontWeight: 600, color: C.muted, textTransform: "uppercase", letterSpacing: 1.6, marginRight: 6 }}>Built with</span>
          {STACK.map((s) => (
            <span key={s} style={{ fontSize: 17, fontWeight: 600, background: "#fff", border: `1px solid ${C.line}`, padding: "8px 14px", borderRadius: 10 }}>{s}</span>
          ))}
        </div>
      </div>

      {/* product shots */}
      {wide ? (
        <>
          <div style={{ position: "absolute", left: 980, top: 150, transform: "perspective(2200px) rotateY(-9deg) rotateX(2deg)", transformOrigin: "left center" }}>
            <Browser width={1180} src="overview.png" ratio={1720 / 2720} />
          </div>
          <div style={{ position: "absolute", left: 880, top: 790, width: 680, borderRadius: 18, border: `1px solid ${C.line}`,
            boxShadow: "0 30px 60px -18px rgba(15,17,21,0.32)", background: "#fff", padding: "16px 18px 14px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 15, fontWeight: 700, color: C.violet, marginBottom: 10 }}>
              <span style={{ width: 8, height: 8, borderRadius: 4, background: C.violet }} /> AI reply forecast
            </div>
            <Img src={staticFile("reply_card.png")} style={{ width: 644, display: "block" }} />
          </div>
        </>
      ) : (
        <>
          <div style={{ position: "absolute", left: pad, top: 640 }}>
            <Browser width={1280} src="overview.png" ratio={1720 / 2720} />
          </div>
          <div style={{ position: "absolute", right: 40, top: 880, width: 640, borderRadius: 18, border: `1px solid ${C.line}`,
            boxShadow: "0 30px 60px -18px rgba(15,17,21,0.32)", background: "#fff", padding: "16px 18px 14px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 15, fontWeight: 700, color: C.violet, marginBottom: 10 }}>
              <span style={{ width: 8, height: 8, borderRadius: 4, background: C.violet }} /> AI reply forecast
            </div>
            <Img src={staticFile("reply_card.png")} style={{ width: 604, display: "block" }} />
          </div>
        </>
      )}
    </AbsoluteFill>
  );
};
