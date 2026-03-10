import { useState, useEffect, useRef } from "react";

// ── Math helpers ─────────────────────────────────────────────────────
const gaussPDF = (x, mu = 0, sigma = 1) =>
  (1 / (sigma * Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * ((x - mu) / sigma) ** 2);

const gaussCDF = (x, mu = 0, sigma = 1) => {
  const z = (x - mu) / (sigma * Math.sqrt(2));
  return 0.5 * (1 + erf(z));
};

function erf(x) {
  const a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911;
  const sign = x < 0 ? -1 : 1;
  const t = 1 / (1 + p * Math.abs(x));
  const y = 1 - ((((a5*t+a4)*t+a3)*t+a2)*t+a1)*t*Math.exp(-x*x);
  return sign * y;
}

function buildPoints(fn, xMin, xMax, steps = 300) {
  const pts = [];
  for (let i = 0; i <= steps; i++) {
    const x = xMin + (i / steps) * (xMax - xMin);
    pts.push({ x, y: fn(x) });
  }
  return pts;
}

function toSVG(pt, xMin, xMax, yMin, yMax, W, H, padX, padY) {
  const sx = padX + ((pt.x - xMin) / (xMax - xMin)) * (W - 2 * padX);
  const sy = H - padY - ((pt.y - yMin) / (yMax - yMin)) * (H - 2 * padY);
  return { sx, sy };
}

function pointsToPath(pts, xMin, xMax, yMin, yMax, W, H, padX, padY) {
  return pts.map((p, i) => {
    const { sx, sy } = toSVG(p, xMin, xMax, yMin, yMax, W, H, padX, padY);
    return `${i === 0 ? "M" : "L"} ${sx.toFixed(1)},${sy.toFixed(1)}`;
  }).join(" ");
}

function areaPath(pts, xMin, xMax, yMin, yMax, W, H, padX, padY) {
  const base = H - padY;
  const first = toSVG(pts[0], xMin, xMax, yMin, yMax, W, H, padX, padY);
  const last = toSVG(pts[pts.length - 1], xMin, xMax, yMin, yMax, W, H, padX, padY);
  const line = pts.map((p, i) => {
    const { sx, sy } = toSVG(p, xMin, xMax, yMin, yMax, W, H, padX, padY);
    return `${i === 0 ? "M" : "L"} ${sx.toFixed(1)},${sy.toFixed(1)}`;
  }).join(" ");
  return `${line} L ${last.sx.toFixed(1)},${base} L ${first.sx.toFixed(1)},${base} Z`;
}

// ── Shared styles ───────────────────────────────────────────────────
const C = {
  bg: "#07080D",
  panel: "#0F1118",
  panelBorder: "#1E2235",
  text: "#E2E4F0",
  muted: "#5A5F7A",
  accent: "#5E8BFF",
  gold: "#F0C040",
  green: "#34D399",
  rose: "#F87171",
  teal: "#2DD4BF",
  purple: "#A78BFA",
  orange: "#FB923C",
};

const tag = (label, color) => (
  <span style={{
    background: `${color}22`, border: `1px solid ${color}55`,
    color, padding: "2px 10px", borderRadius: 3, fontSize: 11,
    letterSpacing: 1, fontWeight: 700, textTransform: "uppercase",
  }}>{label}</span>
);

const sectionLabel = (text, color = C.accent) => (
  <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
    <div style={{ width: 3, height: 28, background: color, borderRadius: 2 }} />
    <span style={{ fontSize: 18, fontWeight: 700, color, fontFamily: "'Palatino Linotype', Palatino, serif", letterSpacing: -0.3 }}>{text}</span>
  </div>
);

const callout = (emoji, title, lines, color = C.accent) => (
  <div style={{
    background: `${color}0D`, border: `1px solid ${color}33`,
    borderRadius: 8, padding: "14px 16px", marginTop: 14,
  }}>
    <div style={{ fontSize: 13, fontWeight: 700, color, marginBottom: 6 }}>{emoji}  {title}</div>
    {lines.map((l, i) => <div key={i} style={{ fontSize: 12.5, color: "#B0B4CC", lineHeight: 1.7, marginBottom: 2 }}>• {l}</div>)}
  </div>
);

const pill = (label, val, color) => (
  <div style={{
    display: "flex", flexDirection: "column", alignItems: "center",
    background: `${color}11`, border: `1px solid ${color}33`,
    borderRadius: 8, padding: "10px 16px", minWidth: 90,
  }}>
    <span style={{ fontSize: 18, fontWeight: 700, color, fontFamily: "Palatino, serif" }}>{val}</span>
    <span style={{ fontSize: 10, color: C.muted, letterSpacing: 1, textTransform: "uppercase", marginTop: 2 }}>{label}</span>
  </div>
);

// ── SECTION 1: Random Variable ───────────────────────────────────────
function SecRandomVar() {
  const [rolling, setRolling] = useState(false);
  const [results, setResults] = useState([]);
  const [current, setCurrent] = useState(null);
  const intervalRef = useRef(null);

  const roll = () => {
    if (rolling) return;
    setRolling(true);
    let count = 0;
    const maxRolls = 30;
    intervalRef.current = setInterval(() => {
      const v = Math.ceil(Math.random() * 6);
      setCurrent(v);
      count++;
      if (count >= maxRolls) {
        clearInterval(intervalRef.current);
        setRolling(false);
        setResults(prev => [...prev, v]);
      }
    }, 60);
  };

  const reset = () => { setResults([]); setCurrent(null); };

  const freq = [1,2,3,4,5,6].map(v => ({ v, count: results.filter(r => r === v).length }));
  const maxFreq = Math.max(1, ...freq.map(f => f.count));

  return (
    <div>
      {sectionLabel("What is a Random Variable?", C.accent)}

      <p style={{ fontSize: 13.5, color: "#B0B4CC", lineHeight: 1.8, marginBottom: 16 }}>
        A <strong style={{ color: C.text }}>random variable</strong> is a variable whose value is determined by chance.
        You cannot know what it will be before it happens — but you <em style={{ color: C.gold }}>can know the probabilities</em> of each outcome.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 20 }}>
        {/* Dice sim */}
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 20 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 16 }}>
            Live Example — Dice Roll
          </div>
          <div style={{
            width: 80, height: 80, margin: "0 auto 16px",
            background: `${C.accent}15`, border: `2px solid ${C.accent}44`,
            borderRadius: 12, display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 40, transition: "all 0.1s",
            boxShadow: current ? `0 0 20px ${C.accent}33` : "none",
          }}>
            {["⚀","⚁","⚂","⚃","⚄","⚅"][current - 1] || "🎲"}
          </div>
          <div style={{ display: "flex", gap: 8, justifyContent: "center" }}>
            <button onClick={roll} disabled={rolling} style={{
              padding: "8px 20px", borderRadius: 6, border: "none",
              background: rolling ? "#333" : C.accent, color: rolling ? "#666" : "#fff",
              cursor: rolling ? "not-allowed" : "pointer", fontSize: 13, fontWeight: 600,
            }}>
              {rolling ? "Rolling..." : "Roll!"}
            </button>
            <button onClick={reset} style={{
              padding: "8px 16px", borderRadius: 6, border: `1px solid ${C.panelBorder}`,
              background: "transparent", color: C.muted, cursor: "pointer", fontSize: 13,
            }}>Reset</button>
          </div>
          <div style={{ textAlign: "center", marginTop: 10, fontSize: 12, color: C.muted }}>
            {results.length} rolls recorded
          </div>
        </div>

        {/* Frequency chart */}
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 20 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>
            Observed Frequency
          </div>
          <div style={{ display: "flex", alignItems: "flex-end", gap: 6, height: 80, marginBottom: 8 }}>
            {freq.map(({ v, count }) => (
              <div key={v} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 3 }}>
                <div style={{ fontSize: 10, color: C.accent }}>{count > 0 ? count : ""}</div>
                <div style={{
                  width: "100%", background: `${C.accent}88`,
                  height: `${(count / maxFreq) * 64}px`,
                  minHeight: count > 0 ? 4 : 0,
                  borderRadius: "3px 3px 0 0", transition: "height 0.3s",
                }} />
              </div>
            ))}
          </div>
          <div style={{ display: "flex", gap: 6 }}>
            {freq.map(({ v }) => (
              <div key={v} style={{ flex: 1, textAlign: "center", fontSize: 14, color: C.muted }}>
                {["⚀","⚁","⚂","⚃","⚄","⚅"][v-1]}
              </div>
            ))}
          </div>
          <div style={{ marginTop: 10, fontSize: 11, color: C.muted, lineHeight: 1.6 }}>
            Each face has probability = 1/6 ≈ 0.167. As rolls increase, the bars approach equal height — that is the probability distribution!
          </div>
        </div>
      </div>

      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 18 }}>
        <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>
          Random Variable vs Fixed Variable
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          {[
            { label: "FIXED Variable", ex: "π = 3.14159...", desc: "Always the same value. No randomness. You know it before measuring.", color: C.muted },
            { label: "RANDOM Variable", ex: "Result of dice roll", desc: "Different each time. You can only know the PROBABILITY of each outcome.", color: C.accent },
          ].map(row => (
            <div key={row.label} style={{
              background: `${row.color}0A`, border: `1px solid ${row.color}33`,
              borderRadius: 8, padding: 14,
            }}>
              <div style={{ fontSize: 11, color: row.color, fontWeight: 700, letterSpacing: 1, textTransform: "uppercase", marginBottom: 6 }}>{row.label}</div>
              <div style={{ fontSize: 16, color: row.color, fontFamily: "Palatino, serif", marginBottom: 6 }}>{row.ex}</div>
              <div style={{ fontSize: 12, color: "#9094AA", lineHeight: 1.6 }}>{row.desc}</div>
            </div>
          ))}
        </div>
      </div>

      {callout("🎯", "Key Properties of a Random Variable",
        ["It maps outcomes (Ω) to numbers — e.g., number of heads in 3 coin flips: {HHH→3, HHT→2, HTH→2...}",
          "It does NOT return a probability — it returns a NUMBER. The probability measure P assigns probabilities.",
          "Examples: tomorrow's temperature, height of a random person, number of cars passing a street in 1 hour."],
        C.accent)}
    </div>
  );
}

// ── SECTION 2: CDF ───────────────────────────────────────────────────
function SecCDF() {
  const [xVal, setXVal] = useState(0);
  const W = 420, H = 200, PX = 30, PY = 20;
  const xMin = -3.5, xMax = 3.5;

  const cdfPts = buildPoints(x => gaussCDF(x), xMin, xMax);
  const pdfPts = buildPoints(x => gaussPDF(x), xMin, xMax);
  const prob = gaussCDF(xVal);

  const xSVG = PX + ((xVal - xMin) / (xMax - xMin)) * (W - 2 * PX);

  const pdfAreaPts = buildPoints(x => x <= xVal ? gaussPDF(x) : 0, xMin, xVal > xMin ? xVal : xMin + 0.001, 200);

  return (
    <div>
      {sectionLabel("Cumulative Distribution Function (CDF)", C.teal)}

      <p style={{ fontSize: 13.5, color: "#B0B4CC", lineHeight: 1.8, marginBottom: 16 }}>
        The CDF answers one question: <strong style={{ color: C.gold }}>"What is the probability that my variable is AT MOST x?"</strong><br />
        Formally: <span style={{ fontFamily: "Palatino, serif", color: C.teal, fontSize: 15 }}>F(x) = P(X ≤ x)</span>
      </p>

      {/* Interactive slider */}
      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 20, marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase" }}>
            Interactive — Drag to see P(X ≤ x)
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            {pill("x value", xVal.toFixed(2), C.teal)}
            {pill("P(X ≤ x)", prob.toFixed(3), C.gold)}
          </div>
        </div>

        <input type="range" min="-3.5" max="3.5" step="0.05" value={xVal}
          onChange={e => setXVal(parseFloat(e.target.value))}
          style={{ width: "100%", accentColor: C.teal, marginBottom: 16 }} />

        {/* Two charts side by side */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          {/* PDF with shaded area */}
          <div>
            <div style={{ fontSize: 11, color: C.muted, textAlign: "center", marginBottom: 6 }}>PDF — shaded area = P(X ≤ {xVal.toFixed(1)})</div>
            <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", overflow: "visible" }}>
              <defs>
                <linearGradient id="pdfGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={C.gold} stopOpacity="0.6" />
                  <stop offset="100%" stopColor={C.gold} stopOpacity="0.05" />
                </linearGradient>
              </defs>
              <line x1={PX} y1={H-PY} x2={W-PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1" />
              {[-3,-2,-1,0,1,2,3].map(v => {
                const sx = PX + ((v - xMin) / (xMax - xMin)) * (W - 2 * PX);
                return <g key={v}>
                  <line x1={sx} y1={H-PY} x2={sx} y2={H-PY+4} stroke="#2A2D3E" strokeWidth="1"/>
                  <text x={sx} y={H-PY+13} textAnchor="middle" fontSize="9" fill="#3A3D52">{v}</text>
                </g>;
              })}
              {/* Shaded area */}
              {xVal > xMin && (
                <path
                  d={areaPath(
                    buildPoints(x => gaussPDF(x), xMin, xVal, 200),
                    xMin, xVal, 0, 0.42, W, H, PX, PY
                  )}
                  fill="url(#pdfGrad)"
                />
              )}
              {/* Full PDF curve */}
              <path d={pointsToPath(pdfPts, xMin, xMax, 0, 0.42, W, H, PX, PY)}
                fill="none" stroke={C.teal} strokeWidth="2" strokeLinecap="round" />
              {/* Vertical line at x */}
              <line x1={xSVG} y1={PY} x2={xSVG} y2={H - PY} stroke={C.gold} strokeWidth="1.5" strokeDasharray="4 3" />
              <text x={xSVG + 4} y={PY + 12} fontSize="10" fill={C.gold}>x = {xVal.toFixed(1)}</text>
              <text x={(PX + xSVG) / 2} y={H/2 + 10} textAnchor="middle" fontSize="11" fill={C.gold} fontWeight="bold">
                {(prob * 100).toFixed(1)}%
              </text>
            </svg>
          </div>

          {/* CDF curve */}
          <div>
            <div style={{ fontSize: 11, color: C.muted, textAlign: "center", marginBottom: 6 }}>CDF — value at x = P(X ≤ {xVal.toFixed(1)})</div>
            <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", overflow: "visible" }}>
              <line x1={PX} y1={H-PY} x2={W-PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1" />
              {[-3,-2,-1,0,1,2,3].map(v => {
                const sx = PX + ((v - xMin) / (xMax - xMin)) * (W - 2 * PX);
                return <g key={v}>
                  <line x1={sx} y1={H-PY} x2={sx} y2={H-PY+4} stroke="#2A2D3E" strokeWidth="1"/>
                  <text x={sx} y={H-PY+13} textAnchor="middle" fontSize="9" fill="#3A3D52">{v}</text>
                </g>;
              })}
              {[0,0.25,0.5,0.75,1.0].map(v => {
                const sy = H - PY - v * (H - 2 * PY);
                return <g key={v}>
                  <line x1={PX} y1={sy} x2={PX - 4} y2={sy} stroke="#2A2D3E" strokeWidth="1"/>
                  <text x={PX - 6} y={sy + 3} textAnchor="end" fontSize="8" fill="#3A3D52">{v}</text>
                </g>;
              })}
              <path d={pointsToPath(cdfPts, xMin, xMax, 0, 1, W, H, PX, PY)}
                fill="none" stroke={C.teal} strokeWidth="2" strokeLinecap="round" />
              {/* Crosshairs */}
              <line x1={xSVG} y1={H-PY-prob*(H-2*PY)} x2={PX} y2={H-PY-prob*(H-2*PY)}
                stroke={C.gold} strokeWidth="1" strokeDasharray="3 3" />
              <line x1={xSVG} y1={PY} x2={xSVG} y2={H-PY}
                stroke={C.gold} strokeWidth="1" strokeDasharray="4 3" />
              <circle cx={xSVG} cy={H-PY-prob*(H-2*PY)} r={4} fill={C.gold} />
              <text x={PX + 4} y={H-PY-prob*(H-2*PY)-4} fontSize="10" fill={C.gold}>F(x) = {prob.toFixed(3)}</text>
            </svg>
          </div>
        </div>
      </div>

      {/* Properties table */}
      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 18 }}>
        <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 14 }}>
          CDF Properties — Quartiles
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10 }}>
          {[
            { label: "F(x) range", val: "[0, 1]", note: "Always a probability", color: C.teal },
            { label: "Q1", val: "F(q₁) = 0.25", note: "25% of data below Q1", color: C.accent },
            { label: "Q2 (Median)", val: "F(q₂) = 0.50", note: "50% of data below", color: C.gold },
            { label: "Q3", val: "F(q₃) = 0.75", note: "75% of data below Q3", color: C.orange },
          ].map(item => (
            <div key={item.label} style={{
              background: `${item.color}0A`, border: `1px solid ${item.color}33`,
              borderRadius: 8, padding: 12, textAlign: "center",
            }}>
              <div style={{ fontSize: 10, color: item.color, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, marginBottom: 4 }}>{item.label}</div>
              <div style={{ fontSize: 13, color: item.color, fontFamily: "Palatino, serif", marginBottom: 4 }}>{item.val}</div>
              <div style={{ fontSize: 11, color: C.muted }}>{item.note}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── SECTION 3: PDF ───────────────────────────────────────────────────
function SecPDF() {
  const [a, setA] = useState(-1);
  const [b, setB] = useState(1);
  const W = 500, H = 200, PX = 30, PY = 20;
  const xMin = -3.5, xMax = 3.5;

  const lo = Math.min(a, b), hi = Math.max(a, b);
  const prob = gaussCDF(hi) - gaussCDF(lo);
  const pdfPts = buildPoints(x => gaussPDF(x), xMin, xMax);

  const loX = PX + ((lo - xMin) / (xMax - xMin)) * (W - 2 * PX);
  const hiX = PX + ((hi - xMin) / (xMax - xMin)) * (W - 2 * PX);

  return (
    <div>
      {sectionLabel("Probability Density Function (PDF)", C.purple)}

      <p style={{ fontSize: 13.5, color: "#B0B4CC", lineHeight: 1.8, marginBottom: 16 }}>
        The PDF is the <strong style={{ color: C.text }}>continuous version of a frequency histogram</strong> — it describes the <em style={{ color: C.gold }}>relative likelihood</em> of the variable taking a given value.
        <br />Key insight: <strong style={{ color: C.purple }}>P(a ≤ X ≤ b) = the AREA under the curve between a and b.</strong>
      </p>

      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 20, marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase" }}>
            Drag sliders — area between a and b = P(a ≤ X ≤ b)
          </div>
          <div style={{
            background: `${C.purple}22`, border: `1px solid ${C.purple}55`,
            borderRadius: 8, padding: "8px 16px", textAlign: "center",
          }}>
            <div style={{ fontSize: 11, color: C.muted, marginBottom: 2 }}>P({lo.toFixed(1)} ≤ X ≤ {hi.toFixed(1)})</div>
            <div style={{ fontSize: 22, fontWeight: 700, color: C.purple, fontFamily: "Palatino, serif" }}>
              {(prob * 100).toFixed(1)}%
            </div>
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 14 }}>
          <div>
            <label style={{ fontSize: 11, color: C.rose, display: "block", marginBottom: 4 }}>a = {a.toFixed(2)}</label>
            <input type="range" min="-3.5" max="3.5" step="0.05" value={a}
              onChange={e => setA(parseFloat(e.target.value))}
              style={{ width: "100%", accentColor: C.rose }} />
          </div>
          <div>
            <label style={{ fontSize: 11, color: C.green, display: "block", marginBottom: 4 }}>b = {b.toFixed(2)}</label>
            <input type="range" min="-3.5" max="3.5" step="0.05" value={b}
              onChange={e => setB(parseFloat(e.target.value))}
              style={{ width: "100%", accentColor: C.green }} />
          </div>
        </div>

        <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", overflow: "visible" }}>
          <defs>
            <linearGradient id="areaG" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={C.purple} stopOpacity="0.55" />
              <stop offset="100%" stopColor={C.purple} stopOpacity="0.05" />
            </linearGradient>
          </defs>
          <line x1={PX} y1={H-PY} x2={W-PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1" />
          {[-3,-2,-1,0,1,2,3].map(v => {
            const sx = PX + ((v - xMin) / (xMax - xMin)) * (W - 2 * PX);
            return <g key={v}>
              <line x1={sx} y1={H-PY} x2={sx} y2={H-PY+4} stroke="#2A2D3E" strokeWidth="1"/>
              <text x={sx} y={H-PY+14} textAnchor="middle" fontSize="10" fill="#4A4D62">{v}σ</text>
            </g>;
          })}
          {/* Shaded area */}
          {hi > lo && (
            <path
              d={areaPath(buildPoints(x => gaussPDF(x), lo, hi, 200), lo, hi, 0, 0.42, W, H, PX, PY)}
              fill="url(#areaG)"
            />
          )}
          <path d={pointsToPath(pdfPts, xMin, xMax, 0, 0.42, W, H, PX, PY)}
            fill="none" stroke={C.purple} strokeWidth="2.5" strokeLinecap="round" />
          <line x1={loX} y1={PY} x2={loX} y2={H-PY} stroke={C.rose} strokeWidth="1.5" strokeDasharray="4 3" />
          <line x1={hiX} y1={PY} x2={hiX} y2={H-PY} stroke={C.green} strokeWidth="1.5" strokeDasharray="4 3" />
          <text x={loX} y={PY - 4} textAnchor="middle" fontSize="10" fill={C.rose} fontWeight="bold">a={lo.toFixed(1)}</text>
          <text x={hiX} y={PY - 4} textAnchor="middle" fontSize="10" fill={C.green} fontWeight="bold">b={hi.toFixed(1)}</text>
          <text x={(loX+hiX)/2} y={H/2} textAnchor="middle" fontSize="13" fill={C.purple} fontWeight="bold">
            {(prob*100).toFixed(1)}%
          </text>
        </svg>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>
            PDF Properties
          </div>
          {[
            { prop: "p(x) ≥ 0", desc: "Density is never negative (but CAN exceed 1!)" },
            { prop: "∫p(x)dx = 1", desc: "Total area under curve always = 100%" },
            { prop: "P(X = exact value)", desc: "= 0 for continuous variables! Only intervals have probability." },
            { prop: "P(a ≤ X ≤ b)", desc: "= area under curve from a to b = ∫p(x)dx" },
          ].map(row => (
            <div key={row.prop} style={{ display: "flex", gap: 10, marginBottom: 10 }}>
              <code style={{ fontSize: 12, color: C.purple, background: `${C.purple}15`, padding: "2px 6px", borderRadius: 3, whiteSpace: "nowrap" }}>{row.prop}</code>
              <span style={{ fontSize: 12, color: "#9094AA", lineHeight: 1.5 }}>{row.desc}</span>
            </div>
          ))}
        </div>

        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>
            PDF vs Histogram
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {[
              { label: "Histogram", desc: "Discrete bars — shows counts or proportions for each bin", color: C.orange },
              { label: "PDF", desc: "Smooth continuous curve — limit of histogram as bin width → 0", color: C.purple },
              { label: "Both show", desc: "Where data is concentrated — peaks = most likely values", color: C.green },
              { label: "Key diff", desc: "PDF y-axis is 'density', not probability. Area gives probability.", color: C.gold },
            ].map(row => (
              <div key={row.label} style={{ display: "flex", gap: 8, padding: "6px 10px", background: `${row.color}0A`, borderRadius: 6 }}>
                <span style={{ fontSize: 11, color: row.color, fontWeight: 700, minWidth: 70 }}>{row.label}</span>
                <span style={{ fontSize: 12, color: "#9094AA", lineHeight: 1.5 }}>{row.desc}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ── SECTION 4: Gaussian ──────────────────────────────────────────────
function SecGaussian() {
  const [mu, setMu] = useState(0);
  const [sigma, setSigma] = useState(1);
  const W = 460, H = 200, PX = 30, PY = 20;
  const xMin = -6, xMax = 6;

  const pdfPts = buildPoints(x => gaussPDF(x, mu, sigma), xMin, xMax);
  const yMax = gaussPDF(mu, mu, sigma) * 1.15;

  const bands = [
    { z: 1.64, pct: "90%", color: "#F0C04033" },
    { z: 1.96, pct: "95%", color: "#5E8BFF33" },
    { z: 2.58, pct: "99%", color: "#34D39933" },
  ];

  return (
    <div>
      {sectionLabel("Gaussian (Normal) Distribution", C.gold)}

      <p style={{ fontSize: 13.5, color: "#B0B4CC", lineHeight: 1.8, marginBottom: 16 }}>
        The Gaussian distribution is the famous <strong style={{ color: C.text }}>bell curve</strong>. It is completely described by just two numbers:
        <strong style={{ color: C.gold }}> μ (mean)</strong> — where the peak sits, and <strong style={{ color: C.rose }}>σ (standard deviation)</strong> — how wide or narrow the bell is.
      </p>

      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 20, marginBottom: 16 }}>
        <div style={{ display: "flex", gap: 16, marginBottom: 14, flexWrap: "wrap" }}>
          <div style={{ flex: 1, minWidth: 180 }}>
            <label style={{ fontSize: 11, color: C.gold, display: "block", marginBottom: 4 }}>
              μ (mean) = {mu.toFixed(1)} — moves the curve LEFT/RIGHT
            </label>
            <input type="range" min="-3" max="3" step="0.1" value={mu}
              onChange={e => setMu(parseFloat(e.target.value))}
              style={{ width: "100%", accentColor: C.gold }} />
          </div>
          <div style={{ flex: 1, minWidth: 180 }}>
            <label style={{ fontSize: 11, color: C.rose, display: "block", marginBottom: 4 }}>
              σ (std dev) = {sigma.toFixed(1)} — makes the curve NARROW/WIDE
            </label>
            <input type="range" min="0.3" max="2.5" step="0.1" value={sigma}
              onChange={e => setSigma(parseFloat(e.target.value))}
              style={{ width: "100%", accentColor: C.rose }} />
          </div>
          <button onClick={() => { setMu(0); setSigma(1); }} style={{
            padding: "6px 14px", borderRadius: 6, border: `1px solid ${C.panelBorder}`,
            background: "transparent", color: C.muted, cursor: "pointer", fontSize: 12, alignSelf: "flex-end",
          }}>Reset to N(0,1)</button>
        </div>

        <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", overflow: "visible" }}>
          <defs>
            {bands.map((b, i) => (
              <linearGradient key={i} id={`bg${i}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={b.color.slice(0, 7)} stopOpacity="0.25" />
                <stop offset="100%" stopColor={b.color.slice(0, 7)} stopOpacity="0.02" />
              </linearGradient>
            ))}
          </defs>
          <line x1={PX} y1={H-PY} x2={W-PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1" />
          {[-5,-4,-3,-2,-1,0,1,2,3,4,5].map(v => {
            const sx = PX + ((v - xMin) / (xMax - xMin)) * (W - 2 * PX);
            return <g key={v}>
              <line x1={sx} y1={H-PY} x2={sx} y2={H-PY+4} stroke="#2A2D3E" strokeWidth="1"/>
              <text x={sx} y={H-PY+13} textAnchor="middle" fontSize="9" fill="#3A3D52">{v}</text>
            </g>;
          })}
          {/* Coloured bands — fixed at μ ± z*σ */}
          {[...bands].reverse().map((b, i) => {
            const lo = mu - b.z * sigma, hi = mu + b.z * sigma;
            if (lo < xMin || hi > xMax) return null;
            const lx = PX + ((lo - xMin) / (xMax - xMin)) * (W - 2 * PX);
            const rx = PX + ((hi - xMin) / (xMax - xMin)) * (W - 2 * PX);
            return <rect key={i} x={lx} y={PY} width={rx - lx} height={H - PY - PY}
              fill={`url(#bg${2 - i})`} />;
          })}
          <path d={pointsToPath(pdfPts, xMin, xMax, 0, yMax, W, H, PX, PY)}
            fill="none" stroke={C.gold} strokeWidth="2.5" strokeLinecap="round" />
          {/* μ line */}
          {(() => {
            const mx = PX + ((mu - xMin) / (xMax - xMin)) * (W - 2 * PX);
            return <line x1={mx} y1={PY} x2={mx} y2={H-PY} stroke={C.gold} strokeWidth="1.5" strokeDasharray="4 3" />;
          })()}
        </svg>

        {/* 90/95/99 legend */}
        <div style={{ display: "flex", gap: 12, justifyContent: "center", marginTop: 10, flexWrap: "wrap" }}>
          {bands.map(b => (
            <div key={b.pct} style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <div style={{ width: 12, height: 12, background: b.color.slice(0,7), opacity: 0.7, borderRadius: 2 }} />
              <span style={{ fontSize: 11, color: C.muted }}>μ ± {b.z}σ = <strong style={{ color: C.text }}>{b.pct}</strong></span>
            </div>
          ))}
        </div>
      </div>

      {/* Properties grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12, marginBottom: 16 }}>
        {[
          { label: "90% of data within", val: "μ ± 1.64σ", color: C.gold },
          { label: "95% of data within", val: "μ ± 1.96σ", color: C.accent, note: "← basis of 95% CI!" },
          { label: "99% of data within", val: "μ ± 2.58σ", color: C.green },
        ].map(item => (
          <div key={item.label} style={{
            background: `${item.color}0F`, border: `1px solid ${item.color}44`,
            borderRadius: 8, padding: "14px 12px", textAlign: "center",
          }}>
            <div style={{ fontSize: 11, color: item.color, textTransform: "uppercase", letterSpacing: 1, marginBottom: 6 }}>{item.label}</div>
            <div style={{ fontSize: 16, color: item.color, fontFamily: "Palatino, serif", fontWeight: 700 }}>{item.val}</div>
            {item.note && <div style={{ fontSize: 10, color: C.accent, marginTop: 4 }}>{item.note}</div>}
          </div>
        ))}
      </div>

      {/* Standardisation */}
      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 18 }}>
        <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 14 }}>
          Standardisation — Converting Any Normal to N(0,1)
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
          <div>
            <div style={{ fontFamily: "Palatino, serif", fontSize: 18, color: C.teal, textAlign: "center", padding: "12px", background: `${C.teal}0F`, borderRadius: 8, marginBottom: 10 }}>
              X̃ = (X − μ) / σ
            </div>
            <div style={{ fontSize: 12, color: "#9094AA", lineHeight: 1.7 }}>
              Step 1: Subtract μ — moves the peak to zero.<br />
              Step 2: Divide by σ — scales so std dev = 1.
            </div>
          </div>
          <div>
            {[
              { label: "X ~ N(5, 4)", desc: "A normal with mean 5, variance 4 (σ=2)" },
              { label: "X̃ = (X-5)/2", desc: "Subtract mean 5, divide by σ=2" },
              { label: "X̃ ~ N(0, 1)", desc: "Now it's the standard normal!" },
            ].map((row, i) => (
              <div key={i} style={{ display: "flex", gap: 8, marginBottom: 8 }}>
                <code style={{ fontSize: 12, color: C.teal, background: `${C.teal}15`, padding: "2px 8px", borderRadius: 3, whiteSpace: "nowrap" }}>{row.label}</code>
                <span style={{ fontSize: 12, color: "#9094AA" }}>{row.desc}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ── SECTION 5: CLT ───────────────────────────────────────────────────
function SecCLT() {
  const [n, setN] = useState(5);
  const [samples, setSamples] = useState([]);
  const [running, setRunning] = useState(false);
  const runRef = useRef(null);

  const generate = () => {
    const newSamples = [];
    for (let i = 0; i < 800; i++) {
      let sum = 0;
      for (let j = 0; j < n; j++) sum += Math.random(); // Uniform [0,1]
      newSamples.push(sum / n);
    }
    setSamples(newSamples);
  };

  useEffect(() => { generate(); }, [n]);

  const numBins = 30;
  const binMin = 0, binMax = 1;
  const bins = Array(numBins).fill(0);
  samples.forEach(s => {
    const idx = Math.min(numBins - 1, Math.floor((s - binMin) / (binMax - binMin) * numBins));
    if (idx >= 0) bins[idx]++;
  });
  const maxBin = Math.max(1, ...bins);

  const W = 460, H = 160;

  return (
    <div>
      {sectionLabel("Central Limit Theorem (CLT)", C.green)}

      <p style={{ fontSize: 13.5, color: "#B0B4CC", lineHeight: 1.8, marginBottom: 16 }}>
        The CLT says: if you take the <strong style={{ color: C.text }}>average of n independent random variables</strong>, the result approaches a <strong style={{ color: C.green }}>Gaussian distribution</strong> as n grows — <em style={{ color: C.gold }}>no matter what shape the original distribution has.</em>
      </p>

      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 20, marginBottom: 16 }}>
        <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }}>
          Live Demo — Averaging n Uniform Random Variables
        </div>
        <div style={{ fontSize: 12, color: "#7A7D96", marginBottom: 14 }}>
          Each individual variable is UNIFORM (flat rectangle — not Gaussian at all). Watch what happens to the distribution of their <em>average</em> as n grows.
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 16, flexWrap: "wrap" }}>
          <div style={{ flex: 1, minWidth: 200 }}>
            <label style={{ fontSize: 11, color: C.green, display: "block", marginBottom: 4 }}>
              n = {n} variables averaged per sample
            </label>
            <input type="range" min="1" max="30" step="1" value={n}
              onChange={e => setN(parseInt(e.target.value))}
              style={{ width: "100%", accentColor: C.green }} />
          </div>
          <button onClick={generate} style={{
            padding: "8px 18px", borderRadius: 6, border: "none",
            background: C.green, color: "#000", cursor: "pointer",
            fontSize: 13, fontWeight: 700,
          }}>Regenerate</button>
          <div style={{
            background: n >= 10 ? `${C.green}15` : `${C.rose}15`,
            border: `1px solid ${n >= 10 ? C.green : C.rose}44`,
            borderRadius: 8, padding: "8px 14px", textAlign: "center",
          }}>
            <div style={{ fontSize: 11, color: C.muted, marginBottom: 2 }}>CLT Active?</div>
            <div style={{ fontSize: 14, fontWeight: 700, color: n >= 10 ? C.green : C.rose }}>
              {n >= 10 ? "✓ YES" : `Need n > 10`}
            </div>
          </div>
        </div>

        {/* Histogram */}
        <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", marginBottom: 8 }}>
          {bins.map((count, i) => {
            const bx = 30 + (i / numBins) * (W - 60);
            const bw = (W - 60) / numBins - 1;
            const bh = (count / maxBin) * (H - 40);
            const hue = n < 5 ? C.rose : n < 10 ? C.orange : C.green;
            return (
              <rect key={i} x={bx} y={H - 30 - bh} width={bw} height={bh}
                fill={hue} opacity="0.75" rx="1" />
            );
          })}
          <line x1={30} y1={H-30} x2={W-30} y2={H-30} stroke="#2A2D3E" strokeWidth="1" />
          {[0, 0.25, 0.5, 0.75, 1].map(v => {
            const sx = 30 + v * (W - 60);
            return <g key={v}>
              <text x={sx} y={H-18} textAnchor="middle" fontSize="9" fill="#4A4D62">{v.toFixed(2)}</text>
            </g>;
          })}
          {/* Overlay Gaussian */}
          {n >= 5 && (() => {
            const mean = 0.5;
            const sd = 1 / Math.sqrt(12 * n);
            const pts = buildPoints(x => gaussPDF(x, mean, sd), binMin, binMax, 200);
            const scale = (maxBin / samples.length) * numBins * (binMax - binMin) / (H - 40) * (H - 40);
            const path = pts.map((p, i) => {
              const sx = 30 + ((p.x - binMin) / (binMax - binMin)) * (W - 60);
              const sy = H - 30 - (p.y * (samples.length / numBins) * ((binMax - binMin) / numBins) / maxBin * (H - 40));
              return `${i === 0 ? "M" : "L"} ${sx.toFixed(1)},${sy.toFixed(1)}`;
            }).join(" ");
            return <path d={path} fill="none" stroke="white" strokeWidth="1.5" strokeDasharray="4 3" opacity="0.5" />;
          })()}
          <text x={30} y={15} fontSize="11" fill={C.muted}>Distribution of sample means (n={n}, 800 samples)</text>
        </svg>

        <div style={{ fontSize: 11, color: C.muted, textAlign: "center" }}>
          {n === 1 && "n=1: Single uniform variable — flat rectangle. No bell shape."}
          {n > 1 && n < 5 && "n=2-4: Triangular shape emerging. Getting slightly bell-like."}
          {n >= 5 && n < 10 && "n=5-9: Clearly bell-shaped already! CLT kicking in."}
          {n >= 10 && "n≥10: Very close to perfect Gaussian. White dashed = predicted bell curve. They match!"}
        </div>
      </div>

      {/* Summary */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>What CLT States</div>
          {[
            { q: "Original distribution?", a: "Can be ANYTHING — uniform, skewed, bimodal, etc." },
            { q: "What converges?", a: "The distribution of the SUM or AVERAGE of n samples" },
            { q: "Converges to?", a: "A Gaussian / Normal distribution" },
            { q: "When?", a: "As n → ∞. In practice: n > 30 usually sufficient" },
          ].map(row => (
            <div key={row.q} style={{ marginBottom: 10 }}>
              <div style={{ fontSize: 11, color: C.green, fontWeight: 700, marginBottom: 2 }}>{row.q}</div>
              <div style={{ fontSize: 12, color: "#9094AA" }}>{row.a}</div>
            </div>
          ))}
        </div>

        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>Why It Matters</div>
          {[
            { icon: "🌍", text: "Many natural phenomena are sums of many small effects → Gaussian. Height = sum of many genetic + environmental factors." },
            { icon: "📊", text: "Justifies using normal distribution tools (confidence intervals, z-scores) even when original data is not normal — as long as n is large." },
            { icon: "⚠️", text: "Warning: CLT does NOT work for very small n. And some heavy-tailed distributions need much larger n." },
            { icon: "🔀", text: "A mixture of 2 Gaussians is NOT a Gaussian — do not confuse mixture models with CLT!" },
          ].map(row => (
            <div key={row.icon} style={{ display: "flex", gap: 8, marginBottom: 10 }}>
              <span style={{ fontSize: 16 }}>{row.icon}</span>
              <span style={{ fontSize: 12, color: "#9094AA", lineHeight: 1.5 }}>{row.text}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── SECTION 6: Confidence Intervals ─────────────────────────────────
function SecCI() {
  const [n, setN] = useState(25);
  const [phat, setPhat] = useState(0.75);
  const [conf, setConf] = useState(95);

  const z = conf === 90 ? 1.64 : conf === 95 ? 1.96 : 2.58;
  const se = Math.sqrt((phat * (1 - phat)) / n);
  const lo = Math.max(0, phat - z * se);
  const hi = Math.min(1, phat + z * se);
  const width = hi - lo;

  const W = 460, H = 60;
  const barX = 30, barW = W - 60;
  const loX = barX + lo * barW;
  const hiX = barX + hi * barW;
  const pX = barX + phat * barW;

  return (
    <div>
      {sectionLabel("Estimations & Confidence Intervals", C.orange)}

      <p style={{ fontSize: 13.5, color: "#B0B4CC", lineHeight: 1.8, marginBottom: 16 }}>
        We never have access to the full population — we work with a <strong style={{ color: C.text }}>sample</strong>.
        A confidence interval gives a <strong style={{ color: C.orange }}>range of plausible values</strong> for the true population parameter, along with how confident we are.
      </p>

      {/* Standard Error explainer */}
      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 18, marginBottom: 16 }}>
        <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 14 }}>
          Standard Error — How reliable is our estimate?
        </div>
        <div style={{ fontFamily: "Palatino, serif", fontSize: 18, color: C.orange, textAlign: "center", padding: "12px", background: `${C.orange}0F`, borderRadius: 8, marginBottom: 14 }}>
          SE = σ / √n
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10 }}>
          {[
            { n: 10,   se: (1/Math.sqrt(10)).toFixed(3), note: "Small sample — unreliable" },
            { n: 100,  se: (1/Math.sqrt(100)).toFixed(3), note: "Medium sample" },
            { n: 1000, se: (1/Math.sqrt(1000)).toFixed(3), note: "Large sample — very reliable" },
          ].map(row => (
            <div key={row.n} style={{
              background: `${C.orange}0A`, border: `1px solid ${C.orange}33`,
              borderRadius: 8, padding: 12, textAlign: "center",
            }}>
              <div style={{ fontSize: 11, color: C.muted, marginBottom: 4 }}>n = {row.n}</div>
              <div style={{ fontSize: 18, fontWeight: 700, color: C.orange, fontFamily: "Palatino, serif" }}>SE = {row.se}</div>
              <div style={{ fontSize: 11, color: C.muted, marginTop: 4 }}>{row.note}</div>
            </div>
          ))}
        </div>
        <div style={{ fontSize: 12, color: "#7A7D96", marginTop: 12, textAlign: "center" }}>
          To HALVE the SE, you must QUADRUPLE the sample size. (SE ∝ 1/√n)
        </div>
      </div>

      {/* Interactive CI builder */}
      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 20, marginBottom: 16 }}>
        <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 14 }}>
          Interactive — 95% CI for Proportion (The Shampoo Example)
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12, marginBottom: 16 }}>
          <div>
            <label style={{ fontSize: 11, color: C.orange, display: "block", marginBottom: 4 }}>Sample size n = {n}</label>
            <input type="range" min="5" max="500" step="5" value={n}
              onChange={e => setN(parseInt(e.target.value))}
              style={{ width: "100%", accentColor: C.orange }} />
          </div>
          <div>
            <label style={{ fontSize: 11, color: C.gold, display: "block", marginBottom: 4 }}>Observed p̂ = {phat.toFixed(2)}</label>
            <input type="range" min="0.1" max="0.99" step="0.01" value={phat}
              onChange={e => setPhat(parseFloat(e.target.value))}
              style={{ width: "100%", accentColor: C.gold }} />
          </div>
          <div>
            <label style={{ fontSize: 11, color: C.teal, display: "block", marginBottom: 4 }}>Confidence level</label>
            <div style={{ display: "flex", gap: 6 }}>
              {[90, 95, 99].map(c => (
                <button key={c} onClick={() => setConf(c)} style={{
                  flex: 1, padding: "6px 0", borderRadius: 4,
                  border: `1px solid ${conf === c ? C.teal : C.panelBorder}`,
                  background: conf === c ? `${C.teal}22` : "transparent",
                  color: conf === c ? C.teal : C.muted, cursor: "pointer", fontSize: 12,
                }}>{c}%</button>
              ))}
            </div>
          </div>
        </div>

        {/* CI visual bar */}
        <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", marginBottom: 12 }}>
          {/* Background scale */}
          {[0, 0.25, 0.5, 0.75, 1].map(v => {
            const sx = barX + v * barW;
            return <g key={v}>
              <line x1={sx} y1={10} x2={sx} y2={H-10} stroke="#2A2D3E" strokeWidth="0.5" />
              <text x={sx} y={H-2} textAnchor="middle" fontSize="9" fill="#3A3D52">{(v*100).toFixed(0)}%</text>
            </g>;
          })}
          {/* CI bar */}
          <rect x={loX} y={H/2 - 10} width={hiX - loX} height={20}
            fill={`${C.orange}33`} stroke={C.orange} strokeWidth="1.5" rx="4" />
          {/* p̂ marker */}
          <line x1={pX} y1={H/2 - 14} x2={pX} y2={H/2 + 14} stroke={C.gold} strokeWidth="2.5" />
          <circle cx={pX} cy={H/2} r={4} fill={C.gold} />
          {/* Labels */}
          <text x={loX} y={H/2 - 14} textAnchor="middle" fontSize="9" fill={C.orange}>{(lo*100).toFixed(1)}%</text>
          <text x={hiX} y={H/2 - 14} textAnchor="middle" fontSize="9" fill={C.orange}>{(hi*100).toFixed(1)}%</text>
          <text x={pX} y={H/2 - 16} textAnchor="middle" fontSize="9" fill={C.gold}>p̂={phat.toFixed(2)}</text>
          <text x={(loX+hiX)/2} y={H/2 + 5} textAnchor="middle" fontSize="11" fill={C.orange} fontWeight="bold">
            {(width*100).toFixed(1)} percentage points wide
          </text>
        </svg>

        <div style={{
          background: width > 0.2 ? `${C.rose}0F` : `${C.green}0F`,
          border: `1px solid ${width > 0.2 ? C.rose : C.green}44`,
          borderRadius: 8, padding: "10px 14px",
          display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 8,
        }}>
          <div style={{ fontSize: 13, color: C.text }}>
            <span style={{ color: C.orange, fontWeight: 700 }}>IC{conf}: [{(lo*100).toFixed(1)}%, {(hi*100).toFixed(1)}%]</span>
            <span style={{ color: C.muted, marginLeft: 10, fontSize: 12 }}>width = {(width*100).toFixed(1)}pp</span>
          </div>
          <div style={{ fontSize: 12, color: width > 0.2 ? C.rose : C.green }}>
            {width > 0.3 ? "⚠️ Very wide — sample too small, do NOT trust this claim!" :
             width > 0.15 ? "⚠️ Wide interval — results are uncertain" :
             "✓ Reasonable interval — results are informative"}
          </div>
        </div>

        <div style={{ marginTop: 10, fontSize: 12, color: "#7A7D96", fontStyle: "italic" }}>
          Try n=25, p̂=0.75 (the shampoo example from lecture). You get [58%, 92%] — a 34pp range that is useless!
          Then try n=500 to see how a proper sample tightens the interval dramatically.
        </div>
      </div>

      {callout("🥾", "Bootstrap Method — CI for ANYTHING",
        ["Step 1: Take a random sub-sample WITH REPLACEMENT from your n data points.",
          "Step 2: Compute the statistic you want (mean, median, correlation — anything).",
          "Step 3: Repeat 1000+ times to build a distribution of estimates.",
          "Step 4: Sort all estimates. Delete the lowest 2.5% and highest 2.5%.",
          "Step 5: The remaining values define your 95% CI. No formula needed!",
          "'With replacement' = same data point can appear multiple times in one sub-sample."],
        C.green)}
    </div>
  );
}

// ── Graph Reading Helper ─────────────────────────────────────────────
const graphGuide = (lines) => (
  <div style={{
    background: "#0A1628", border: `1px solid ${C.accent}44`,
    borderRadius: 8, padding: "12px 16px", marginBottom: 16,
  }}>
    <div style={{ fontSize: 12, fontWeight: 700, color: C.accent, marginBottom: 8 }}>📖 How to Read This Graph</div>
    {lines.map((l, i) => (
      <div key={i} style={{ fontSize: 12.5, color: "#B0B4CC", lineHeight: 1.7, marginBottom: 3 }}>
        <span style={{ color: C.accent, marginRight: 6 }}>▸</span>{l}
      </div>
    ))}
  </div>
);

const whenToUse = (items, color = C.gold) => (
  <div style={{
    background: `${color}0D`, border: `1px solid ${color}44`,
    borderRadius: 8, padding: "14px 16px", marginTop: 14,
  }}>
    <div style={{ fontSize: 13, fontWeight: 700, color, marginBottom: 8 }}>🗺️ When to Use This — and Why</div>
    {items.map((item, i) => (
      <div key={i} style={{ marginBottom: 10 }}>
        <div style={{ fontSize: 12.5, fontWeight: 700, color, marginBottom: 2 }}>{item.when}</div>
        <div style={{ fontSize: 12, color: "#B0B4CC", lineHeight: 1.6 }}>{item.why}</div>
      </div>
    ))}
  </div>
);

// ── SECTION 7: Bivariate Data ────────────────────────────────────────
function SecBivariate() {
  const DATASETS = {
    positive: { label: "📈 Positive (Study hrs → Score)", xLabel: "Study Hours per Day", yLabel: "Exam Score", color: C.green,
      pts: [[1,45],[2,52],[2,58],[3,61],[3,65],[4,68],[4,72],[5,70],[5,78],[6,80],[6,83],[7,85],[7,88],[8,90],[8,93],[9,91],[9,95],[10,97]] },
    negative: { label: "📉 Negative (Temp → Hot Drinks)", xLabel: "Temperature (°C)", yLabel: "Hot Drinks Sold", color: C.rose,
      pts: [[2,95],[3,90],[5,88],[6,82],[8,78],[10,72],[12,68],[15,60],[18,55],[20,48],[22,45],[24,40],[26,35],[28,30],[30,25],[32,20]] },
    none: { label: "😶 No Correlation (Shoe Size → IQ)", xLabel: "Shoe Size", yLabel: "IQ Score", color: C.muted,
      pts: [[6,88],[6,105],[7,92],[7,115],[7,98],[8,80],[8,102],[8,118],[9,95],[9,88],[9,107],[10,99],[10,112],[10,85],[11,93],[11,108]] },
    nonlinear: { label: "🌀 Non-linear (Sleep → Productivity)", xLabel: "Hours of Sleep", yLabel: "Productivity Score", color: C.purple,
      pts: [[2,30],[3,38],[4,55],[5,72],[6,85],[7,92],[8,90],[9,85],[10,70],[11,55],[12,40],[13,28]] },
  };

  const [dsKey, setDsKey] = useState("positive");
  const [hovIdx, setHovIdx] = useState(null);
  const ds = DATASETS[dsKey];
  const pts = ds.pts;

  const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
  const n = pts.length;
  const meanX = xs.reduce((a,b)=>a+b,0)/n;
  const meanY = ys.reduce((a,b)=>a+b,0)/n;
  const cov = xs.reduce((s,x,i)=>s+(x-meanX)*(ys[i]-meanY),0)/n;
  const varX = xs.reduce((s,x)=>s+(x-meanX)**2,0)/n;
  const varY = ys.reduce((s,y)=>s+(y-meanY)**2,0)/n;
  const r = varX*varY > 0 ? cov/Math.sqrt(varX*varY) : 0;
  const slope = cov / varX;
  const intercept = meanY - slope * meanX;

  const xMin = Math.min(...xs)-1, xMax = Math.max(...xs)+1;
  const yMin = Math.min(...ys)-8, yMax = Math.max(...ys)+8;
  const W = 460, H = 240, PX = 50, PY = 24;

  const toX = x => PX + ((x-xMin)/(xMax-xMin))*(W-2*PX);
  const toY = y => H-PY - ((y-yMin)/(yMax-yMin))*(H-2*PY);

  const rColor = Math.abs(r) > 0.7 ? C.green : Math.abs(r) > 0.4 ? C.gold : C.rose;
  const rLabel = Math.abs(r) > 0.8 ? "Strong" : Math.abs(r) > 0.5 ? "Moderate" : Math.abs(r) > 0.2 ? "Weak" : "None";

  const descs = {
    positive: "The dots go from bottom-left to top-right — as study hours increase, exam scores increase. The dashed line captures this trend. Points close to the line = strong relationship.",
    negative: "The dots go from top-left to bottom-right — as temperature rises, fewer hot drinks are sold. A clear opposite direction relationship.",
    none: "The dots are scattered randomly with no pattern. Knowing someone's shoe size tells you nothing about their IQ. The r value is near 0.",
    nonlinear: "There IS a pattern (an arch), but it's not a straight line. r ≈ 0 because Pearson r only detects straight-line relationships — this is a key limitation!",
  };

  return (
    <div>
      {sectionLabel("Bivariate Data & Scatter Plots", "#E879F9")}

      <div style={{ background: `${"#E879F9"}0D`, border: `1px solid ${"#E879F9"}33`, borderRadius: 8, padding: "14px 16px", marginBottom: 16 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: "#E879F9", marginBottom: 6 }}>🧠 What is bivariate data? (Plain English)</div>
        <div style={{ fontSize: 13, color: "#B0B4CC", lineHeight: 1.8 }}>
          "Bi" means two. Bivariate data = <strong style={{ color: C.text }}>two measurements taken on the same person or thing</strong> at the same time.<br/>
          Example: You weigh 30 students AND measure their heights. That's bivariate — one student, two numbers.<br/>
          The big question is always: <strong style={{ color: C.gold }}>if one variable changes, does the other tend to change too?</strong>
        </div>
      </div>

      {/* Dataset selector */}
      <div style={{ display: "flex", gap: 8, marginBottom: 14, flexWrap: "wrap" }}>
        {Object.entries(DATASETS).map(([k, d]) => (
          <button key={k} onClick={() => setDsKey(k)} style={{
            padding: "7px 14px", borderRadius: 6, border: `1px solid ${dsKey===k ? d.color : C.panelBorder}`,
            background: dsKey===k ? `${d.color}22` : "transparent",
            color: dsKey===k ? d.color : C.muted, cursor: "pointer", fontSize: 12, fontWeight: dsKey===k ? 700 : 400,
            transition: "all 0.15s",
          }}>{d.label}</button>
        ))}
      </div>

      {graphGuide([
        `Each DOT = one person/observation. Its LEFT-RIGHT position = ${ds.xLabel}. Its UP-DOWN position = ${ds.yLabel}.`,
        "To read a dot: trace left to the Y-axis (vertical) to get the Y value. Trace down to the X-axis (horizontal) to get the X value.",
        "The DASHED LINE is the 'line of best fit' — it summarises the trend. If dots cluster tightly around it → strong relationship.",
        "The GOLD dashed cross-hairs mark the average of X and Y. Half the data falls above, half below each line.",
        dsKey === "nonlinear" ? "⚠️ No trend line shown here — there is a curve, not a straight line. r would mislead you." : "The steeper the dashed line, the stronger the effect of X on Y.",
      ])}

      <div style={{ display: "grid", gridTemplateColumns: "3fr 1fr", gap: 16, marginBottom: 14 }}>
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
            <div style={{ fontSize: 11, color: C.muted, letterSpacing: 2, textTransform: "uppercase" }}>Scatter Plot — hover any dot</div>
            <div style={{ fontSize: 11, color: ds.color }}>← X: {ds.xLabel} | Y: {ds.yLabel} ↑</div>
          </div>
          <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", overflow: "visible" }}>
            {[0.25,0.5,0.75].map(t => {
              const gy = PY + t*(H-2*PY);
              return <line key={t} x1={PX} y1={gy} x2={W-PX} y2={gy} stroke="#1A1D2E" strokeWidth="1"/>;
            })}
            <line x1={PX} y1={H-PY} x2={W-PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1.5"/>
            <line x1={PX} y1={PY} x2={PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1.5"/>
            {/* Axis labels */}
            <text x={W/2} y={H+8} textAnchor="middle" fontSize="10" fill="#5A5F7A">→ {ds.xLabel}</text>
            <text x={12} y={H/2} textAnchor="middle" fontSize="10" fill="#5A5F7A" transform={`rotate(-90,12,${H/2})`}>↑ {ds.yLabel}</text>
            {/* Tick marks */}
            {[xMin+1, Math.round((xMin+xMax)/2), Math.round(xMax-1)].map(v => (
              <g key={v}>
                <line x1={toX(v)} y1={H-PY} x2={toX(v)} y2={H-PY+4} stroke="#2A2D3E"/>
                <text x={toX(v)} y={H-PY+14} textAnchor="middle" fontSize="9" fill="#3A3D52">{v}</text>
              </g>
            ))}
            {[Math.round(yMin+5), Math.round((yMin+yMax)/2), Math.round(yMax-5)].map(v => (
              <g key={v}>
                <line x1={PX} y1={toY(v)} x2={PX-4} y2={toY(v)} stroke="#2A2D3E"/>
                <text x={PX-6} y={toY(v)+3} textAnchor="end" fontSize="9" fill="#3A3D52">{v}</text>
              </g>
            ))}
            {/* Regression line */}
            {dsKey !== "nonlinear" && (() => {
              const x1r = xMin, x2r = xMax;
              return <line x1={toX(x1r)} y1={toY(slope*x1r+intercept)} x2={toX(x2r)} y2={toY(slope*x2r+intercept)}
                stroke={ds.color} strokeWidth="2" strokeDasharray="6 3" opacity="0.7"/>;
            })()}
            {/* Mean crosshairs */}
            <line x1={toX(meanX)} y1={PY} x2={toX(meanX)} y2={H-PY} stroke={C.gold} strokeWidth="1" strokeDasharray="3 3" opacity="0.4"/>
            <line x1={PX} y1={toY(meanY)} x2={W-PX} y2={toY(meanY)} stroke={C.gold} strokeWidth="1" strokeDasharray="3 3" opacity="0.4"/>
            <text x={toX(meanX)+4} y={PY+11} fontSize="9" fill={C.gold}>x̄={meanX.toFixed(1)}</text>
            <text x={PX+4} y={toY(meanY)-4} fontSize="9" fill={C.gold}>ȳ={meanY.toFixed(1)}</text>
            {/* Points */}
            {pts.map((p, i) => (
              <g key={i} onMouseEnter={() => setHovIdx(i)} onMouseLeave={() => setHovIdx(null)} style={{cursor:"pointer"}}>
                <circle cx={toX(p[0])} cy={toY(p[1])} r={hovIdx===i ? 7 : 5}
                  fill={hovIdx===i ? ds.color : `${ds.color}88`}
                  stroke={hovIdx===i ? "white" : `${ds.color}44`} strokeWidth="1.5"/>
                {hovIdx===i && <>
                  <line x1={toX(p[0])} y1={toY(p[1])} x2={PX} y2={toY(p[1])} stroke="white" strokeWidth="0.5" strokeDasharray="2 2" opacity="0.4"/>
                  <line x1={toX(p[0])} y1={toY(p[1])} x2={toX(p[0])} y2={H-PY} stroke="white" strokeWidth="0.5" strokeDasharray="2 2" opacity="0.4"/>
                  <rect x={toX(p[0])+10} y={toY(p[1])-22} width={90} height={20} rx="3" fill="#0A0C14" stroke={ds.color} strokeWidth="0.8"/>
                  <text x={toX(p[0])+55} y={toY(p[1])-8} textAnchor="middle" fontSize="10" fill="white" fontWeight="bold">
                    {ds.xLabel.split(" ")[0]}={p[0]}, {ds.yLabel.split(" ")[0]}={p[1]}
                  </text>
                </>}
              </g>
            ))}
          </svg>
          <div style={{ marginTop: 8, padding: "8px 12px", background: `${ds.color}0A`, borderRadius: 6, fontSize: 12, color: "#B0B4CC", lineHeight: 1.6 }}>
            💡 <strong style={{ color: ds.color }}>What you're seeing:</strong> {descs[dsKey]}
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 14, textAlign: "center" }}>
            <div style={{ fontSize: 10, color: C.muted, textTransform: "uppercase", letterSpacing: 1, marginBottom: 4 }}>Correlation r</div>
            <div style={{ fontSize: 34, fontWeight: 700, color: rColor, fontFamily: "Palatino, serif" }}>{r.toFixed(2)}</div>
            <div style={{ fontSize: 12, color: rColor, marginTop: 2 }}>{rLabel}</div>
            <div style={{ fontSize: 11, color: r > 0.1 ? C.green : r < -0.1 ? C.rose : C.muted, marginTop: 2 }}>
              {r > 0.1 ? "↗ Positive" : r < -0.1 ? "↘ Negative" : "↔ No direction"}
            </div>
            <div style={{ width: "100%", height: 6, background: "#1E2235", borderRadius: 3, marginTop: 10, position: "relative" }}>
              <div style={{ width: `${Math.abs(r)*100}%`, height: "100%", background: rColor, borderRadius: 3,
                marginLeft: r < 0 ? `${(1-Math.abs(r))*100}%` : 0 }}/>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 9, color: C.muted, marginTop: 2 }}>
              <span>−1</span><span>0</span><span>+1</span>
            </div>
          </div>
          <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 14 }}>
            <div style={{ fontSize: 10, color: C.muted, textTransform: "uppercase", letterSpacing: 1, marginBottom: 10 }}>Computed Stats</div>
            {[
              { l: "n (pairs)", v: n, c: C.text },
              { l: "mean X (x̄)", v: meanX.toFixed(2), c: C.teal },
              { l: "mean Y (ȳ)", v: meanY.toFixed(2), c: C.teal },
              { l: "Cov(X,Y)", v: cov.toFixed(2), c: "#E879F9" },
              { l: "r² (R-squared)", v: (r*r).toFixed(3), c: C.gold },
            ].map(row => (
              <div key={row.l} style={{ display: "flex", justifyContent: "space-between", marginBottom: 7, paddingBottom: 7, borderBottom: "1px solid #1A1D2E" }}>
                <span style={{ fontSize: 11, color: C.muted }}>{row.l}</span>
                <span style={{ fontSize: 12, color: row.c, fontWeight: 700 }}>{row.v}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 14 }}>
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>What does r actually mean?</div>
          {[
            { r: "r = +1.0", desc: "Dots form a perfect straight line going up-right. Every time X increases, Y increases by an exact fixed amount.", c: C.green },
            { r: "r = +0.8", desc: "Dots are close to a rising line but not perfect. Strong tendency — a clear pattern with some scatter.", c: C.green },
            { r: "r ≈ 0", desc: "Dots are scattered randomly. Knowing X gives you no useful information about Y.", c: C.muted },
            { r: "r = −0.8", desc: "Strong tendency in the opposite direction — as X goes up, Y tends to go down.", c: C.rose },
            { r: "r = −1.0", desc: "Perfect straight line going down-right. Every increase in X means an exact decrease in Y.", c: C.rose },
          ].map(row => (
            <div key={row.r} style={{ display: "flex", gap: 10, marginBottom: 9 }}>
              <code style={{ fontSize: 11, color: row.c, background: `${row.c}15`, padding: "2px 7px", borderRadius: 3, whiteSpace: "nowrap", alignSelf: "flex-start" }}>{row.r}</code>
              <span style={{ fontSize: 12, color: "#9094AA", lineHeight: 1.5 }}>{row.desc}</span>
            </div>
          ))}
        </div>
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>Univariate vs Bivariate — what's the difference?</div>
          {[
            { type: "Univariate", desc: "You measure ONE thing. Example: the heights of 50 students. You can describe it with a mean, histogram, standard deviation.", ex: "📊 'Average height is 170cm, spread is ±8cm'", color: C.accent },
            { type: "Bivariate", desc: "You measure TWO things on the same people. Example: height AND weight of the same 50 students. Now you ask: are taller people heavier?", ex: "🔗 'Height and weight have r = 0.72 — fairly strong link'", color: "#E879F9" },
          ].map(row => (
            <div key={row.type} style={{ background: `${row.color}08`, border: `1px solid ${row.color}33`, borderRadius: 7, padding: "12px", marginBottom: 10 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: row.color, marginBottom: 6 }}>{row.type}</div>
              <div style={{ fontSize: 12, color: "#B0B4CC", marginBottom: 6, lineHeight: 1.6 }}>{row.desc}</div>
              <div style={{ fontSize: 11, color: row.color, fontStyle: "italic" }}>{row.ex}</div>
            </div>
          ))}
        </div>
      </div>

      {whenToUse([
        { when: "Use bivariate analysis when you have two measurements per subject and want to know if they're linked.", why: "Example: A doctor measures patients' blood pressure AND their salt intake. She wants to know: do people who eat more salt tend to have higher blood pressure? Scatter plot + r gives the answer." },
        { when: "Use it before building any prediction model.", why: "If you want to predict exam score from study hours, first check the scatter plot. If the dots look random (r ≈ 0), don't bother building a prediction model — there's nothing to predict from." },
        { when: "Use the 'non-linear' example above as a warning sign.", why: "Always LOOK at your scatter plot before trusting r. If the pattern is curved, r is useless and you need a different approach." },
      ], "#E879F9")}

      {callout("⚠️", "Correlation ≠ Causation — The Most Important Mistake in Statistics",
        ["Both ice cream sales and drowning deaths go up in summer. They're correlated (r ≈ 0.8), but ice cream doesn't cause drowning — both are caused by hot weather (a 'confounder').",
          "r only detects STRAIGHT-LINE patterns. Switch to 'Non-linear' above: there's a clear arch pattern (sleep vs productivity), but r ≈ 0 because it's not a straight line!",
          "Rule of thumb: |r| > 0.7 is strong, 0.4–0.7 is moderate, < 0.4 is weak. But always judge by the scatter plot too — don't just trust the number.",
          "The dashed regression line predicts Y from X, but a prediction is not an explanation. You need a causal theory to claim X causes Y."],
        "#E879F9")}
    </div>
  );
}

// ── SECTION 8: Two-Sample Data ───────────────────────────────────────
function SecTwoSample() {
  const SCENARIOS = {
    ab: {
      label: "🖱️ A/B Test (Button Colour)", xLabel: "Conversion Rate (%)",
      story: "A website shows blue buttons to Group A and red buttons to Group B. Did the colour change affect how many people clicked?",
      A: { label: "Group A (Blue Button)", mu: 12, sigma: 3, color: C.accent, n: 200 },
      B: { label: "Group B (Red Button)", mu: 14.5, sigma: 3.2, color: C.rose, n: 200 },
    },
    drug: {
      label: "💊 Drug Trial (Pain Score)", xLabel: "Pain Score 1–10 (lower = better)",
      story: "50 patients got a placebo (sugar pill) and 50 got the real drug. Did the drug actually reduce pain?",
      A: { label: "Placebo Group", mu: 7.2, sigma: 1.5, color: C.muted, n: 50 },
      B: { label: "Treatment Group", mu: 4.8, sigma: 1.8, color: C.green, n: 50 },
    },
    salary: {
      label: "💰 Salary by Department", xLabel: "Annual Salary (€k)",
      story: "HR wants to know if Department B pays significantly more than Department A, or if the difference is just due to random variation.",
      A: { label: "Department A", mu: 52, sigma: 8, color: C.gold, n: 80 },
      B: { label: "Department B", mu: 58, sigma: 10, color: C.purple, n: 80 },
    },
  };

  const [scKey, setScKey] = useState("ab");
  const sc = SCENARIOS[scKey];

  const xMin = Math.min(sc.A.mu - 3.5*sc.A.sigma, sc.B.mu - 3.5*sc.B.sigma);
  const xMax = Math.max(sc.A.mu + 3.5*sc.A.sigma, sc.B.mu + 3.5*sc.B.sigma);
  const W = 500, H = 190, PX = 30, PY = 24;

  const yMaxA = gaussPDF(sc.A.mu, sc.A.mu, sc.A.sigma);
  const yMaxB = gaussPDF(sc.B.mu, sc.B.mu, sc.B.sigma);
  const yMax = Math.max(yMaxA, yMaxB) * 1.2;

  const ptsA = buildPoints(x => gaussPDF(x, sc.A.mu, sc.A.sigma), xMin, xMax);
  const ptsB = buildPoints(x => gaussPDF(x, sc.B.mu, sc.B.sigma), xMin, xMax);

  const diff = sc.B.mu - sc.A.mu;
  const pooledSE = Math.sqrt(sc.A.sigma**2/sc.A.n + sc.B.sigma**2/sc.B.n);
  const tStat = diff / pooledSE;
  const effectSize = Math.abs(diff) / Math.sqrt((sc.A.sigma**2 + sc.B.sigma**2)/2);
  const significant = Math.abs(tStat) > 1.96;

  return (
    <div>
      {sectionLabel("Two-Sample Data & Comparisons", C.teal)}

      <div style={{ background: `${C.teal}0D`, border: `1px solid ${C.teal}33`, borderRadius: 8, padding: "14px 16px", marginBottom: 16 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: C.teal, marginBottom: 6 }}>🧠 What is two-sample analysis? (Plain English)</div>
        <div style={{ fontSize: 13, color: "#B0B4CC", lineHeight: 1.8 }}>
          You have <strong style={{ color: C.text }}>one measurement</strong> (e.g. salary), but you measure it in <strong style={{ color: C.text }}>two different groups</strong> (e.g. Dept A and Dept B).<br/>
          The question: <strong style={{ color: C.gold }}>Is the gap between the two groups real — or could it just be random luck from small samples?</strong><br/>
          A group of 10 people might differ just by chance. A group of 1000 is much more reliable.
        </div>
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 14, flexWrap: "wrap" }}>
        {Object.entries(SCENARIOS).map(([k, s]) => (
          <button key={k} onClick={() => setScKey(k)} style={{
            padding: "7px 16px", borderRadius: 6,
            border: `1px solid ${scKey===k ? C.teal : C.panelBorder}`,
            background: scKey===k ? `${C.teal}22` : "transparent",
            color: scKey===k ? C.teal : C.muted, cursor: "pointer", fontSize: 12, fontWeight: scKey===k ? 700 : 400,
          }}>{s.label}</button>
        ))}
      </div>

      <div style={{ background: `${C.gold}0A`, border: `1px solid ${C.gold}33`, borderRadius: 7, padding: "10px 14px", marginBottom: 12, fontSize: 12.5, color: "#B0B4CC", lineHeight: 1.7 }}>
        📖 <strong style={{ color: C.gold }}>Scenario:</strong> {sc.story}
      </div>

      {graphGuide([
        "Each CURVE = one group's distribution. Think of it as a smoothed histogram of their measurements.",
        "The PEAK of each curve = where most people in that group scored. The peak's left-right position is the group mean.",
        "A WIDER curve = more spread out scores (high standard deviation). A NARROW curve = scores are consistent.",
        "Where the two curves OVERLAP = the ambiguous zone where you can't easily tell which group a random person belongs to.",
        "The GOLD bracket between the two peak lines = the difference in means (Δ). A bigger gap = a clearer result.",
        "If the curves barely overlap (like the drug trial), the difference is very obvious. If they heavily overlap, it's hard to be sure.",
      ])}

      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 20, marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <div style={{ fontSize: 11, color: C.muted, letterSpacing: 2, textTransform: "uppercase" }}>
            {sc.xLabel}
          </div>
          <div style={{ display: "flex", gap: 12 }}>
            {[sc.A, sc.B].map(g => (
              <div key={g.label} style={{ display: "flex", alignItems: "center", gap: 5 }}>
                <div style={{ width: 10, height: 10, borderRadius: "50%", background: g.color }}/>
                <span style={{ fontSize: 11, color: g.color }}>{g.label} (avg: {g.mu})</span>
              </div>
            ))}
          </div>
        </div>
        <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", overflow: "visible" }}>
          <defs>
            <linearGradient id="gA2" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={sc.A.color} stopOpacity="0.45"/>
              <stop offset="100%" stopColor={sc.A.color} stopOpacity="0.03"/>
            </linearGradient>
            <linearGradient id="gB2" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={sc.B.color} stopOpacity="0.45"/>
              <stop offset="100%" stopColor={sc.B.color} stopOpacity="0.03"/>
            </linearGradient>
          </defs>
          <line x1={PX} y1={H-PY} x2={W-PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1.5"/>
          {/* X labels */}
          {[xMin, (xMin+xMax)/2, xMax].map(v => {
            const sx = PX + ((v-xMin)/(xMax-xMin))*(W-2*PX);
            return <text key={v} x={sx} y={H-PY+14} textAnchor="middle" fontSize="9" fill="#3A3D52">{v.toFixed(1)}</text>;
          })}
          <text x={W/2} y={H+4} textAnchor="middle" fontSize="10" fill="#4A4D62">→ {sc.xLabel}</text>
          {/* Filled areas */}
          <path d={areaPath(ptsA, xMin, xMax, 0, yMax, W, H, PX, PY)} fill="url(#gA2)"/>
          <path d={areaPath(ptsB, xMin, xMax, 0, yMax, W, H, PX, PY)} fill="url(#gB2)"/>
          {/* Curves */}
          <path d={pointsToPath(ptsA, xMin, xMax, 0, yMax, W, H, PX, PY)} fill="none" stroke={sc.A.color} strokeWidth="2.5" strokeLinecap="round"/>
          <path d={pointsToPath(ptsB, xMin, xMax, 0, yMax, W, H, PX, PY)} fill="none" stroke={sc.B.color} strokeWidth="2.5" strokeLinecap="round"/>
          {/* Mean lines with labels */}
          {[sc.A, sc.B].map(g => {
            const mx = PX + ((g.mu - xMin)/(xMax-xMin))*(W-2*PX);
            return <g key={g.label}>
              <line x1={mx} y1={PY} x2={mx} y2={H-PY} stroke={g.color} strokeWidth="1.5" strokeDasharray="5 3"/>
              <text x={mx} y={PY-7} textAnchor="middle" fontSize="10" fill={g.color} fontWeight="bold">mean={g.mu}</text>
            </g>;
          })}
          {/* Diff bracket */}
          {(() => {
            const ax = PX + ((sc.A.mu - xMin)/(xMax-xMin))*(W-2*PX);
            const bx = PX + ((sc.B.mu - xMin)/(xMax-xMin))*(W-2*PX);
            const by = H * 0.55;
            return <g>
              <line x1={ax} y1={by} x2={bx} y2={by} stroke={C.gold} strokeWidth="2"/>
              <line x1={ax} y1={by-6} x2={ax} y2={by+6} stroke={C.gold} strokeWidth="2"/>
              <line x1={bx} y1={by-6} x2={bx} y2={by+6} stroke={C.gold} strokeWidth="2"/>
              <text x={(ax+bx)/2} y={by-8} textAnchor="middle" fontSize="11" fill={C.gold} fontWeight="bold">
                Δ = {diff > 0 ? "+" : ""}{diff.toFixed(1)} (gap between means)
              </text>
            </g>;
          })()}
        </svg>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10, marginBottom: 16 }}>
        {[
          { label: "Mean Gap (Δ)", val: (diff > 0 ? "+" : "")+diff.toFixed(2), color: C.gold,
            note: `${sc.B.label} avg is ${Math.abs(diff).toFixed(1)} units ${diff > 0 ? "higher" : "lower"} than ${sc.A.label}` },
          { label: "t-statistic", val: tStat.toFixed(2), color: Math.abs(tStat)>1.96 ? C.green : C.rose,
            note: `Gap is ${Math.abs(tStat).toFixed(1)}× larger than chance would produce. Need >1.96 to be significant.` },
          { label: "Cohen's d", val: effectSize.toFixed(2), color: effectSize>0.8 ? C.green : effectSize>0.5 ? C.gold : C.orange,
            note: effectSize>0.8?"Large practical effect — noticeable in real life":effectSize>0.5?"Medium effect — somewhat noticeable":"Small effect — hard to notice" },
          { label: "Significant?", val: significant ? "YES ✓" : "NO ✗", color: significant ? C.green : C.rose,
            note: significant ? "The gap is too large to be random chance (95% confident)" : "Could just be random variation — don't conclude a real difference" },
        ].map(item => (
          <div key={item.label} style={{
            background: `${item.color}0A`, border: `1px solid ${item.color}33`, borderRadius: 8, padding: "12px 10px",
          }}>
            <div style={{ fontSize: 10, color: item.color, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, marginBottom: 6 }}>{item.label}</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: item.color, fontFamily: "Palatino, serif", marginBottom: 6 }}>{item.val}</div>
            <div style={{ fontSize: 11, color: C.muted, lineHeight: 1.5 }}>{item.note}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 14 }}>
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>
            Univariate vs Bivariate vs Two-Sample — at a glance
          </div>
          {[
            { type: "Univariate", question: "What does THIS group look like?", ex: "Heights of Class A students", icon: "1️⃣", color: C.accent },
            { type: "Bivariate", question: "Do two things correlate within ONE group?", ex: "Height vs Weight of same students", icon: "🔗", color: "#E879F9" },
            { type: "Two-Sample", question: "Are two groups DIFFERENT from each other?", ex: "Height of Class A vs Class B", icon: "⚖️", color: C.teal },
          ].map(row => (
            <div key={row.type} style={{ background: `${row.color}08`, border: `1px solid ${row.color}33`, borderRadius: 7, padding: "10px 12px", marginBottom: 8 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: row.color, marginBottom: 4 }}>{row.icon} {row.type}</div>
              <div style={{ fontSize: 12, color: "#B0B4CC", marginBottom: 3 }}>❓ <em>{row.question}</em></div>
              <div style={{ fontSize: 11, color: C.muted }}>Example: {row.ex}</div>
            </div>
          ))}
        </div>

        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>
            Reading the t-test result — step by step
          </div>
          {[
            { step: "Step 1", desc: "State H₀: assume the groups are actually the same (μA = μB). This is your starting assumption.", color: C.muted },
            { step: "Step 2", desc: "Calculate Δ = difference in sample means. This is what you observed.", color: C.teal },
            { step: "Step 3", desc: "Calculate t = Δ ÷ SE. This says: 'the gap is t times bigger than random noise'.", color: C.gold },
            { step: "Step 4", desc: "If |t| > 1.96: the gap is so large it would only happen by chance 5% of the time → conclude the groups are different.", color: C.green },
            { step: "Step 5", desc: "Check Cohen's d: even if t is significant, is the effect big enough to matter in practice?", color: C.purple },
          ].map(row => (
            <div key={row.step} style={{ display: "flex", gap: 10, marginBottom: 9 }}>
              <code style={{ fontSize: 11, color: row.color, background: `${row.color}15`, padding: "2px 7px", borderRadius: 3, whiteSpace: "nowrap", alignSelf: "flex-start" }}>{row.step}</code>
              <span style={{ fontSize: 12, color: "#9094AA", lineHeight: 1.5 }}>{row.desc}</span>
            </div>
          ))}
        </div>
      </div>

      {whenToUse([
        { when: "Use two-sample when you're comparing a treatment vs control group.", why: "Drug trials, A/B tests, policy changes — whenever you give different 'treatments' to two groups and want to know if it worked." },
        { when: "Use it when someone shows you two averages and claims one is better.", why: "A company says 'our drug reduced pain from 7.2 to 4.8 on average!' Before believing that, check: is n large enough? Is the t-statistic > 1.96? Is Cohen's d meaningful?" },
        { when: "Be careful with very large samples.", why: "With n=100,000, even a difference of 0.001 will be 'statistically significant'. Always check Cohen's d to see if the effect size is actually meaningful in practice." },
      ], C.teal)}

      {callout("🔬", "Paired vs Independent Samples — a key distinction",
        ["INDEPENDENT: Two completely separate groups (different people). The drug trial example: 50 different people got placebo, 50 different people got the drug.",
          "PAIRED: The SAME people measured twice (e.g. before and after treatment). Paired tests are more powerful because you remove person-to-person variation.",
          "Example: Instead of comparing 50 people before vs 50 different people after, measure the SAME 50 people before and after. Paired t-test is the right tool.",
          "Statistical significance (p < 0.05) just means 'unlikely to be random chance.' It does NOT mean the effect is large or important. Always check effect size too."],
        C.teal)}
    </div>
  );
}

// ── SECTION 9: Covariance (deep dive) ───────────────────────────────
function SecCovariance() {
  const [hovPt, setHovPt] = useState(null);
  const [activeProp, setActiveProp] = useState(0);
  const [showCalc, setShowCalc] = useState(false);

  // Dataset matching the lecture's Figure 2 (μx≈4.9, μy≈3.5)
  const data = [
    { x: 2, y: 1,  label: "A" },
    { x: 3, y: 1,  label: "B" },
    { x: 3, y: 2,  label: "C" },
    { x: 4, y: 4,  label: "D" },
    { x: 5, y: 6,  label: "E" },
    { x: 7, y: 5,  label: "F" },
    { x: 7, y: 4,  label: "G" },
    { x: 9, y: 6,  label: "H" },
  ];
  const n = data.length;
  const meanX = data.reduce((s,d)=>s+d.x,0)/n;
  const meanY = data.reduce((s,d)=>s+d.y,0)/n;
  const rows  = data.map(d => ({
    ...d,
    dx: d.x - meanX,
    dy: d.y - meanY,
    prod: (d.x - meanX) * (d.y - meanY),
  }));
  const cov = rows.reduce((s,r)=>s+r.prod,0)/n;

  const W=460, H=240, PX=44, PY=24;
  const xMin=0, xMax=11, yMin=0, yMax=8;
  const toX = v => PX + (v-xMin)/(xMax-xMin)*(W-2*PX);
  const toY = v => H-PY - (v-yMin)/(yMax-yMin)*(H-2*PY);
  const mxS = toX(meanX), myS = toY(meanY);

  // ── Property demo data ──────────────────────────────────────────────
  const PROPS = [
    {
      id: 0,
      prop: "Cov(X,Y) = Cov(Y,X)",
      title: "Symmetry — order does not matter",
      color: C.teal,
      emoji: "🔄",
      plain: "Swapping which variable is X and which is Y gives you the exact same covariance. The relationship between study hours and score is the same whether you say 'hours vs score' or 'score vs hours'.",
      example: "Cov(Height, Weight) = Cov(Weight, Height). The joint variation is the same either way.",
      why: "Because the formula multiplies (xᵢ−x̄)(yᵢ−ȳ) and multiplication is commutative: a×b = b×a.",
      demo: () => {
        const a = data.map(d=>({x:d.x,y:d.y}));
        const b = data.map(d=>({x:d.y,y:d.x}));
        const cXY = a.reduce((s,d)=>s+(d.x-meanX)*(d.y-meanY),0)/n;
        const mYasX = b.reduce((s,d)=>s+d.x,0)/n;
        const mXasY = b.reduce((s,d)=>s+d.y,0)/n;
        const cYX = b.reduce((s,d)=>s+(d.x-mYasX)*(d.y-mXasY),0)/n;
        return { cXY: cXY.toFixed(3), cYX: cYX.toFixed(3) };
      }
    },
    {
      id: 1,
      prop: "Cov(X,X) = Var(X) = σ²ₓ",
      title: "Variance is a special case of covariance",
      color: C.purple,
      emoji: "🔁",
      plain: "What happens if you compute the covariance of X with itself? You get the variance! This makes sense: 'how much does X move with X?' is exactly the same as 'how spread out is X?'.",
      example: "Var(Height) = Cov(Height, Height). Every point is always in the +,+ or −,− quadrant because both deviations are identical.",
      why: "Cov(X,X) = Σ(xᵢ−x̄)(xᵢ−x̄)/n = Σ(xᵢ−x̄)²/n = Var(X). The formula becomes the variance formula automatically.",
      demo: () => {
        const varX = data.reduce((s,d)=>s+(d.x-meanX)**2,0)/n;
        const covXX = data.reduce((s,d)=>s+(d.x-meanX)*(d.x-meanX),0)/n;
        return { varX: varX.toFixed(3), covXX: covXX.toFixed(3) };
      }
    },
    {
      id: 2,
      prop: "Cov(aX, bY) = ab · Cov(X,Y)",
      title: "Scales with units — the KEY weakness!",
      color: C.rose,
      emoji: "⚠️",
      plain: "If you multiply X by a constant (e.g. convert hours to minutes: multiply by 60), and Y by b, the covariance multiplies by a×b. This means the raw covariance number completely changes just by changing units — even though the real relationship is identical!",
      example: "If X = study hours and you convert to minutes (multiply by 60), Cov becomes 60× bigger. That's why we can't interpret raw covariance size.",
      why: "This is exactly WHY Pearson r was invented: dividing by σₓ×σᵧ cancels the scaling, giving a unit-free number always in [−1,+1].",
      demo: () => {
        const a=60, b=1; // hours → minutes, keep Y same
        const scaledX = data.map(d=>d.x*a);
        const scaledY = data.map(d=>d.y*b);
        const mSX = scaledX.reduce((s,v)=>s+v,0)/n;
        const mSY = scaledY.reduce((s,v)=>s+v,0)/n;
        const covScaled = scaledX.reduce((s,v,i)=>s+(v-mSX)*(scaledY[i]-mSY),0)/n;
        return { original: cov.toFixed(3), scaled: covScaled.toFixed(2), factor: (a*b).toString() };
      }
    },
    {
      id: 3,
      prop: "Cov(a+X, b+Y) = Cov(X,Y)",
      title: "Shift-invariant — adding constants has NO effect",
      color: C.green,
      emoji: "📌",
      plain: "Adding a constant to X (like adding 10 to everyone's score to adjust for a grading curve) has ZERO effect on covariance. The relationship between variables doesn't change when you shift the whole dataset up or down.",
      example: "If every student gets +5 bonus points, the covariance between hours and score stays exactly the same. The deviations from the mean are unchanged.",
      why: "Adding 'a' to X shifts the mean by 'a' too, so the deviation (x+a)−(x̄+a) = x−x̄ is unchanged. The constant cancels out perfectly.",
      demo: () => {
        const a=100, b=50;
        const shiftedX = data.map(d=>d.x+a);
        const shiftedY = data.map(d=>d.y+b);
        const mSX = shiftedX.reduce((s,v)=>s+v,0)/n;
        const mSY = shiftedY.reduce((s,v)=>s+v,0)/n;
        const covShifted = shiftedX.reduce((s,v,i)=>s+(v-mSX)*(shiftedY[i]-mSY),0)/n;
        return { original: cov.toFixed(3), shifted: covShifted.toFixed(3) };
      }
    },
  ];

  const p = PROPS[activeProp];
  const demoResult = p.demo();

  return (
    <div>
      {sectionLabel("Covariance — Full Deep Dive", "#F472B6")}

      {/* ── Big picture explainer ── */}
      <div style={{ background: "#F472B608", border: "1px solid #F472B633", borderRadius: 10, padding: "16px 18px", marginBottom: 20 }}>
        <div style={{ fontSize: 14, fontWeight: 700, color: "#F472B6", marginBottom: 10 }}>🧠 What is Covariance? Start Here.</div>
        <div style={{ fontSize: 13.5, color: "#B0B4CC", lineHeight: 1.9 }}>
          Imagine you measure <strong style={{color:C.text}}>two things about the same person</strong> — say, how many hours they studied (X) and what score they got (Y).
          <br/><strong style={{color:"#F472B6"}}>Covariance asks one question:</strong> <em style={{color:C.gold}}>"When someone studies more than average, do they ALSO tend to score more than average?"</em>
          <br/>If yes → <strong style={{color:C.green}}>positive covariance</strong>. If high X goes with low Y → <strong style={{color:C.rose}}>negative covariance</strong>. If no pattern → <strong style={{color:C.muted}}>covariance near 0</strong>.
          <br/><span style={{color:C.orange, fontWeight:600}}>⚠️ The catch:</span> the raw number depends on the units (hours vs minutes gives different numbers for the same relationship). That's why we need Pearson r — it fixes this.
        </div>
      </div>

      {/* ── Part 1: The Quadrant Diagram (from Image 2) ── */}
      <div style={{ fontSize: 14, fontWeight: 700, color: "#F472B6", marginBottom: 12, display:"flex", alignItems:"center", gap:8 }}>
        <span style={{background:"#F472B622", border:"1px solid #F472B644", borderRadius:6, padding:"2px 10px", fontSize:11}}>PART 1</span>
        The Quadrant Diagram — Why Some Points Help &amp; Some Hurt
      </div>

      <div style={{ background: C.panel, border: "1px solid #F472B633", borderRadius: 10, padding: 20, marginBottom: 20 }}>
        <div style={{ display: "grid", gridTemplateColumns: "3fr 2fr", gap: 20 }}>
          {/* Interactive scatter */}
          <div>
            <div style={{ fontSize: 11, color: C.muted, textTransform:"uppercase", letterSpacing:2, marginBottom:6 }}>
              Figure 2 Recreated — hover each point to see its contribution
            </div>
            <svg viewBox={`0 0 ${W} ${H}`} style={{width:"100%", overflow:"visible"}}>
              {/* Quadrant backgrounds */}
              <rect x={mxS} y={PY} width={W-PX-mxS} height={myS-PY} fill={C.green} opacity="0.07"/>
              <rect x={PX} y={myS} width={mxS-PX} height={H-PY-myS} fill={C.green} opacity="0.07"/>
              <rect x={PX} y={PY} width={mxS-PX} height={myS-PY} fill={C.rose} opacity="0.07"/>
              <rect x={mxS} y={myS} width={W-PX-mxS} height={H-PY-myS} fill={C.rose} opacity="0.07"/>
              {/* Quadrant labels */}
              <text x={mxS+8} y={PY+16} fontSize="10" fill={C.green} opacity="0.9" fontWeight="600">+X,+Y → + contribution</text>
              <text x={PX+5} y={H-PY-8} fontSize="10" fill={C.green} opacity="0.9" fontWeight="600">−X,−Y → + contribution</text>
              <text x={PX+5} y={PY+16} fontSize="10" fill={C.rose} opacity="0.9">−X,+Y → − contribution</text>
              <text x={mxS+8} y={H-PY-8} fontSize="10" fill={C.rose} opacity="0.9">+X,−Y → − contribution</text>
              {/* Axes */}
              <line x1={PX} y1={H-PY} x2={W-PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1.5"/>
              <line x1={PX} y1={PY} x2={PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1.5"/>
              {/* X tick marks */}
              {[2,3,4,5,6,7,8,9,10].map(v=><g key={v}>
                <line x1={toX(v)} y1={H-PY} x2={toX(v)} y2={H-PY+5} stroke="#2A2D3E"/>
                <text x={toX(v)} y={H-PY+14} textAnchor="middle" fontSize="9" fill="#3A3D52">{v}</text>
              </g>)}
              {/* Y tick marks */}
              {[1,2,3,4,5,6,7].map(v=><g key={v}>
                <line x1={PX} y1={toY(v)} x2={PX-5} y2={toY(v)} stroke="#2A2D3E"/>
                <text x={PX-8} y={toY(v)+3} textAnchor="end" fontSize="9" fill="#3A3D52">{v}</text>
              </g>)}
              {/* Mean cross lines */}
              <line x1={mxS} y1={PY} x2={mxS} y2={H-PY} stroke={C.gold} strokeWidth="2" strokeDasharray="6 4"/>
              <line x1={PX} y1={myS} x2={W-PX} y2={myS} stroke={C.gold} strokeWidth="2" strokeDasharray="6 4"/>
              <text x={mxS+4} y={PY-6} fontSize="10" fill={C.gold} fontWeight="700">μₓ = {meanX.toFixed(1)}</text>
              <text x={W-PX-2} y={myS-5} fontSize="10" fill={C.gold} fontWeight="700" textAnchor="end">μᵧ = {meanY.toFixed(1)}</text>
              {/* Deviation rectangle for hovered point */}
              {hovPt !== null && (() => {
                const d = rows[hovPt];
                const x1=Math.min(mxS, toX(d.x)), y1=Math.min(myS, toY(d.y));
                const w=Math.abs(toX(d.x)-mxS), h=Math.abs(toY(d.y)-myS);
                const col = d.prod>=0 ? C.green : C.rose;
                return <rect x={x1} y={y1} width={w} height={h} fill={col} opacity="0.2" stroke={col} strokeWidth="1.5" strokeDasharray="4 2"/>;
              })()}
              {/* Data points */}
              {rows.map((d, i) => {
                const isPos = d.prod >= 0;
                const col = isPos ? C.green : C.rose;
                const hov = hovPt === i;
                return (
                  <g key={i} onMouseEnter={()=>setHovPt(i)} onMouseLeave={()=>setHovPt(null)} style={{cursor:"pointer"}}>
                    <circle cx={toX(d.x)} cy={toY(d.y)} r={hov?9:6}
                      fill={col} stroke={hov?"white":"none"} strokeWidth="2" opacity={hov?1:0.85}/>
                    <text x={toX(d.x)} y={toY(d.y)-11} textAnchor="middle" fontSize="10" fill={col} fontWeight="700">{d.label}</text>
                  </g>
                );
              })}
              {/* Axis labels */}
              <text x={W/2} y={H+10} textAnchor="middle" fontSize="11" fill={C.muted}>X</text>
              <text x={12} y={H/2} textAnchor="middle" fontSize="11" fill={C.muted} transform={`rotate(-90,12,${H/2})`}>Y</text>
            </svg>
            <div style={{display:"flex", gap:14, marginTop:8, justifyContent:"center"}}>
              <div style={{display:"flex", alignItems:"center", gap:5}}>
                <div style={{width:10,height:10,borderRadius:"50%",background:C.green}}/>
                <span style={{fontSize:11,color:C.green}}>Positive contribution (same side of means)</span>
              </div>
              <div style={{display:"flex", alignItems:"center", gap:5}}>
                <div style={{width:10,height:10,borderRadius:"50%",background:C.rose}}/>
                <span style={{fontSize:11,color:C.rose}}>Negative contribution (opposite sides)</span>
              </div>
            </div>
          </div>

          {/* Detail panel */}
          <div style={{display:"flex", flexDirection:"column", gap:10}}>
            {/* Hovered point detail */}
            <div style={{background:"#0F1118", border:`1px solid ${hovPt!==null?(rows[hovPt].prod>=0?C.green:C.rose):C.panelBorder}`, borderRadius:8, padding:14, minHeight:160}}>
              {hovPt !== null ? (() => {
                const d = rows[hovPt];
                const col = d.prod>=0 ? C.green : C.rose;
                return <>
                  <div style={{fontSize:13,fontWeight:700,color:col,marginBottom:8}}>Point {d.label}: ({d.x}, {d.y})</div>
                  <div style={{fontSize:12,color:"#B0B4CC",lineHeight:1.8}}>
                    <span style={{color:C.teal}}>X deviation:</span> {d.x} − {meanX.toFixed(1)} = <strong style={{color:d.dx>=0?C.green:C.rose}}>{d.dx>=0?"+":""}{d.dx.toFixed(2)}</strong><br/>
                    <span style={{color:C.purple}}>Y deviation:</span> {d.y} − {meanY.toFixed(1)} = <strong style={{color:d.dy>=0?C.green:C.rose}}>{d.dy>=0?"+":""}{d.dy.toFixed(2)}</strong><br/>
                    <span style={{color:col}}>Product:</span> ({d.dx>=0?"+":""}{d.dx.toFixed(2)}) × ({d.dy>=0?"+":""}{d.dy.toFixed(2)}) = <strong style={{color:col}}>{d.prod>=0?"+":""}{d.prod.toFixed(2)}</strong>
                  </div>
                  <div style={{marginTop:10, padding:"8px 10px", background:`${col}11`, borderRadius:6, fontSize:12, color:col}}>
                    {d.prod>=0
                      ? d.dx>0 ? "✅ Both ABOVE average → positive contribution" : "✅ Both BELOW average → positive contribution"
                      : "❌ Opposite sides of mean → negative contribution"}
                  </div>
                </>;
              })() : (
                <div style={{fontSize:12,color:C.muted,textAlign:"center",marginTop:40}}>
                  👆 Hover over a point<br/>to see its contribution<br/>to covariance
                </div>
              )}
            </div>
            {/* Running total */}
            <div style={{background:"#0F1118", border:"1px solid #F472B633", borderRadius:8, padding:14}}>
              <div style={{fontSize:11,color:C.muted,textTransform:"uppercase",letterSpacing:1,marginBottom:8}}>All Contributions</div>
              {rows.map((d,i) => (
                <div key={i} style={{display:"flex",justifyContent:"space-between",marginBottom:5,opacity:hovPt===i?1:0.65}}>
                  <span style={{fontSize:11,color:C.text,fontWeight:hovPt===i?700:400}}>Point {d.label}</span>
                  <div style={{display:"flex",gap:8,alignItems:"center"}}>
                    <div style={{width:50,height:6,background:"#1E2235",borderRadius:3,overflow:"hidden"}}>
                      <div style={{width:`${Math.min(100,Math.abs(d.prod)/3*100)}%`,height:"100%",background:d.prod>=0?C.green:C.rose,borderRadius:3}}/>
                    </div>
                    <span style={{fontSize:11,color:d.prod>=0?C.green:C.rose,fontWeight:700,minWidth:42,textAlign:"right"}}>{d.prod>=0?"+":""}{d.prod.toFixed(2)}</span>
                  </div>
                </div>
              ))}
              <div style={{borderTop:"1px solid #1E2235",marginTop:8,paddingTop:8,display:"flex",justifyContent:"space-between"}}>
                <span style={{fontSize:12,color:C.gold,fontWeight:700}}>Cov(X,Y) = average</span>
                <span style={{fontSize:14,color:C.gold,fontWeight:700}}>{cov.toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Reading the diagram — step-by-step box */}
        <div style={{marginTop:16, background:"#0A0C15", border:"1px solid #F472B622", borderRadius:8, padding:"12px 16px"}}>
          <div style={{fontSize:12,fontWeight:700,color:"#F472B6",marginBottom:10}}>📖 How to Read the Quadrant Diagram (step by step)</div>
          <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10}}>
            {[
              {step:"① Draw mean lines",desc:"Draw a vertical line at μₓ and a horizontal line at μᵧ. These split the plot into 4 quadrants.",color:C.gold},
              {step:"② Label quadrants",desc:"Top-right (+,+): both above means. Bottom-left (−,−): both below. Top-left (−,+) and Bottom-right (+,−): opposite sides.",color:C.teal},
              {step:"③ Colour each point",desc:"Green if the point is in (+,+) or (−,−). Red if in (−,+) or (+,−). Green points add positively, red points subtract.",color:C.green},
              {step:"④ Average = Cov",desc:"Multiply each point's two deviations together, sum them up, divide by n. That average is the covariance!",color:"#F472B6"},
            ].map(s=>(
              <div key={s.step} style={{background:`${s.color}0A`,border:`1px solid ${s.color}33`,borderRadius:7,padding:10}}>
                <div style={{fontSize:11,color:s.color,fontWeight:700,marginBottom:5}}>{s.step}</div>
                <div style={{fontSize:11,color:"#9094AA",lineHeight:1.6}}>{s.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Part 2: The 4 Properties (from Image 1) ── */}
      <div style={{ fontSize: 14, fontWeight: 700, color: "#F472B6", marginBottom: 12, display:"flex", alignItems:"center", gap:8 }}>
        <span style={{background:"#F472B622", border:"1px solid #F472B644", borderRadius:6, padding:"2px 10px", fontSize:11}}>PART 2</span>
        Section 2.3 — The 4 Properties, Explained with Examples
      </div>

      {/* Property selector tabs */}
      <div style={{display:"flex", gap:6, marginBottom:14, flexWrap:"wrap"}}>
        {PROPS.map((p,i) => (
          <button key={i} onClick={()=>setActiveProp(i)} style={{
            padding:"8px 14px", borderRadius:7, cursor:"pointer", fontSize:12, fontWeight:activeProp===i?700:400,
            border:`1px solid ${activeProp===i?p.color:C.panelBorder}`,
            background:activeProp===i?`${p.color}22`:"transparent",
            color:activeProp===i?p.color:C.muted, transition:"all 0.15s",
          }}>{p.emoji} {p.prop}</button>
        ))}
      </div>

      <div style={{background:C.panel, border:`1px solid ${p.color}44`, borderRadius:10, padding:20, marginBottom:16}}>
        <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:20}}>
          {/* Left: full explanation */}
          <div>
            <div style={{fontFamily:"Palatino, serif", fontSize:20, color:p.color, textAlign:"center", padding:"12px 16px", background:`${p.color}0F`, borderRadius:8, marginBottom:14}}>
              {p.prop}
            </div>
            <div style={{fontSize:13, fontWeight:700, color:p.color, marginBottom:8}}>{p.emoji} {p.title}</div>

            <div style={{background:"#0A0C15", border:`1px solid ${p.color}22`, borderRadius:7, padding:"12px 14px", marginBottom:12}}>
              <div style={{fontSize:11, color:C.muted, textTransform:"uppercase", letterSpacing:1, marginBottom:6}}>Plain English</div>
              <div style={{fontSize:13, color:"#B0B4CC", lineHeight:1.8}}>{p.plain}</div>
            </div>

            <div style={{background:"#0A0C15", border:`1px solid ${C.gold}22`, borderRadius:7, padding:"12px 14px", marginBottom:12}}>
              <div style={{fontSize:11, color:C.gold, textTransform:"uppercase", letterSpacing:1, marginBottom:6}}>Real-World Example</div>
              <div style={{fontSize:13, color:"#B0B4CC", lineHeight:1.8}}>{p.example}</div>
            </div>

            <div style={{background:"#0A0C15", border:`1px solid ${C.teal}22`, borderRadius:7, padding:"12px 14px"}}>
              <div style={{fontSize:11, color:C.teal, textTransform:"uppercase", letterSpacing:1, marginBottom:6}}>Why it works (maths)</div>
              <div style={{fontSize:13, color:"#B0B4CC", lineHeight:1.8}}>{p.why}</div>
            </div>
          </div>

          {/* Right: live demo result */}
          <div style={{display:"flex", flexDirection:"column", gap:12}}>
            <div style={{fontSize:12, color:C.muted, textTransform:"uppercase", letterSpacing:1, marginBottom:2}}>Live Proof with our Dataset</div>

            {activeProp === 0 && (
              <div style={{background:"#0A0C15", borderRadius:8, padding:16}}>
                <div style={{fontSize:12,color:C.muted,marginBottom:12}}>Compute Cov(X,Y) then Cov(Y,X) — should be the same:</div>
                {[
                  {label:"Cov(X,Y) — X=hours, Y=score", val:demoResult.cXY, color:C.teal},
                  {label:"Cov(Y,X) — X=score, Y=hours", val:demoResult.cYX, color:C.purple},
                ].map(row=>(
                  <div key={row.label} style={{background:`${row.color}0A`,border:`1px solid ${row.color}33`,borderRadius:7,padding:12,marginBottom:8}}>
                    <div style={{fontSize:11,color:row.color,marginBottom:4}}>{row.label}</div>
                    <div style={{fontSize:26,fontWeight:700,color:row.color,fontFamily:"Palatino,serif"}}>{row.val}</div>
                  </div>
                ))}
                <div style={{padding:"10px 12px",background:`${C.green}0F`,border:`1px solid ${C.green}33`,borderRadius:6,fontSize:12,color:C.green,marginTop:4}}>
                  ✅ Identical! Order doesn't matter.
                </div>
              </div>
            )}

            {activeProp === 1 && (
              <div style={{background:"#0A0C15", borderRadius:8, padding:16}}>
                <div style={{fontSize:12,color:C.muted,marginBottom:12}}>Compute Var(X) and Cov(X,X) — should match:</div>
                {[
                  {label:"Var(X) = Σ(xᵢ−x̄)² / n", val:demoResult.varX, color:C.teal},
                  {label:"Cov(X,X) = Σ(xᵢ−x̄)(xᵢ−x̄) / n", val:demoResult.covXX, color:C.purple},
                ].map(row=>(
                  <div key={row.label} style={{background:`${row.color}0A`,border:`1px solid ${row.color}33`,borderRadius:7,padding:12,marginBottom:8}}>
                    <div style={{fontSize:11,color:row.color,marginBottom:4}}>{row.label}</div>
                    <div style={{fontSize:26,fontWeight:700,color:row.color,fontFamily:"Palatino,serif"}}>{row.val}</div>
                  </div>
                ))}
                <div style={{padding:"10px 12px",background:`${C.green}0F`,border:`1px solid ${C.green}33`,borderRadius:6,fontSize:12,color:C.green,marginTop:4}}>
                  ✅ Identical! Variance is covariance with itself.
                </div>
              </div>
            )}

            {activeProp === 2 && (
              <div style={{background:"#0A0C15", borderRadius:8, padding:16}}>
                <div style={{fontSize:12,color:C.muted,marginBottom:12}}>Convert X from hours to minutes (×60). Y unchanged (×1):</div>
                {[
                  {label:"Original Cov(X, Y)", val:demoResult.original, note:"X in hours", color:C.teal},
                  {label:"Cov(60X, Y) after scaling", val:demoResult.scaled, note:`Expected: ${demoResult.factor} × original = ${(parseFloat(demoResult.original)*60).toFixed(2)}`, color:C.rose},
                ].map(row=>(
                  <div key={row.label} style={{background:`${row.color}0A`,border:`1px solid ${row.color}33`,borderRadius:7,padding:12,marginBottom:8}}>
                    <div style={{fontSize:11,color:row.color,marginBottom:4}}>{row.label}</div>
                    <div style={{fontSize:26,fontWeight:700,color:row.color,fontFamily:"Palatino,serif"}}>{row.val}</div>
                    <div style={{fontSize:10,color:C.muted,marginTop:4}}>{row.note}</div>
                  </div>
                ))}
                <div style={{padding:"10px 12px",background:`${C.rose}0F`,border:`1px solid ${C.rose}33`,borderRadius:6,fontSize:12,color:C.rose,marginTop:4}}>
                  ⚠️ Same relationship, but Cov changed 60×! This is why raw Cov is hard to interpret.
                </div>
              </div>
            )}

            {activeProp === 3 && (
              <div style={{background:"#0A0C15", borderRadius:8, padding:16}}>
                <div style={{fontSize:12,color:C.muted,marginBottom:12}}>Add 100 to all X values, add 50 to all Y values:</div>
                {[
                  {label:"Original Cov(X, Y)", val:demoResult.original, note:"X: 2–9, Y: 1–6", color:C.teal},
                  {label:"Cov(100+X, 50+Y)", val:demoResult.shifted, note:"X: 102–109, Y: 51–56", color:C.green},
                ].map(row=>(
                  <div key={row.label} style={{background:`${row.color}0A`,border:`1px solid ${row.color}33`,borderRadius:7,padding:12,marginBottom:8}}>
                    <div style={{fontSize:11,color:row.color,marginBottom:4}}>{row.label}</div>
                    <div style={{fontSize:26,fontWeight:700,color:row.color,fontFamily:"Palatino,serif"}}>{row.val}</div>
                    <div style={{fontSize:10,color:C.muted,marginTop:4}}>{row.note}</div>
                  </div>
                ))}
                <div style={{padding:"10px 12px",background:`${C.green}0F`,border:`1px solid ${C.green}33`,borderRadius:6,fontSize:12,color:C.green,marginTop:4}}>
                  ✅ Identical! Shifting data up/down doesn't change the relationship.
                </div>
              </div>
            )}

            {/* Summary badge */}
            <div style={{background:`${p.color}0A`, border:`1px solid ${p.color}33`, borderRadius:8, padding:"12px 14px"}}>
              <div style={{fontSize:11,color:p.color,fontWeight:700,textTransform:"uppercase",letterSpacing:1,marginBottom:6}}>Key Takeaway</div>
              {activeProp===0 && <div style={{fontSize:12,color:"#B0B4CC",lineHeight:1.7}}>Cov is symmetric. You can always write it either way — Cov(X,Y) or Cov(Y,X). No difference.</div>}
              {activeProp===1 && <div style={{fontSize:12,color:"#B0B4CC",lineHeight:1.7}}>Variance IS covariance. Var(X) = Cov(X,X). One formula unifies both concepts.</div>}
              {activeProp===2 && <div style={{fontSize:12,color:"#B0B4CC",lineHeight:1.7}}>The big weakness: Cov depends on units. Always convert to Pearson r for interpretation.</div>}
              {activeProp===3 && <div style={{fontSize:12,color:"#B0B4CC",lineHeight:1.7}}>Shifting data (adding constants) doesn't change the relationship — deviations are unaffected.</div>}
            </div>
          </div>
        </div>
      </div>

      {/* All 4 properties summary table */}
      <div style={{background:C.panel, border:"1px solid #F472B633", borderRadius:10, padding:16, marginBottom:14}}>
        <div style={{fontSize:12,color:C.muted,textTransform:"uppercase",letterSpacing:2,marginBottom:14}}>Summary — All 4 Properties at a Glance (Section 2.3)</div>
        <table style={{width:"100%",borderCollapse:"collapse"}}>
          <thead>
            <tr style={{background:"#13162088"}}>
              <th style={{padding:"10px 14px",color:C.text,textAlign:"left",fontSize:12,fontWeight:700,borderBottom:"1px solid #1E2235"}}>Property</th>
              <th style={{padding:"10px 14px",color:C.text,textAlign:"left",fontSize:12,fontWeight:700,borderBottom:"1px solid #1E2235"}}>Meaning</th>
              <th style={{padding:"10px 14px",color:C.text,textAlign:"left",fontSize:12,fontWeight:700,borderBottom:"1px solid #1E2235"}}>Why it matters</th>
            </tr>
          </thead>
          <tbody>
            {[
              {prop:"Cov(X,Y) = Cov(Y,X)", meaning:"Symmetric — order does not matter", why:"Safe to write either way. Correlation matrices are therefore also symmetric.", color:C.teal},
              {prop:"Cov(X,X) = Var(X) = σ²ₓ", meaning:"Variance is a special case of covariance", why:"Variance and covariance share one unified formula. Variance = covariance with yourself.", color:C.purple},
              {prop:"Cov(aX, bY) = ab·Cov(X,Y)", meaning:"Scales with both variables' units — KEY weakness!", why:"Raw covariance is uninterpretable across different units. Pearson r solves this.", color:C.rose},
              {prop:"Cov(a+X, b+Y) = Cov(X,Y)", meaning:"Shift-invariant: adding constants has no effect", why:"Centering or shifting your data doesn't destroy covariance. Useful for normalisation.", color:C.green},
            ].map((row,i)=>(
              <tr key={i} style={{borderBottom:"1px solid #12141E", background:activeProp===i?`${row.color}08`:"transparent"}}>
                <td style={{padding:"10px 14px"}}>
                  <code style={{fontSize:12,color:row.color,background:`${row.color}15`,padding:"3px 8px",borderRadius:4}}>{row.prop}</code>
                </td>
                <td style={{padding:"10px 14px",fontSize:12,color:"#B0B4CC",lineHeight:1.6}}>{row.meaning}</td>
                <td style={{padding:"10px 14px",fontSize:12,color:"#9094AA",lineHeight:1.6}}>{row.why}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <CovUsageExamples />
    </div>
  );
}

// ── Interactive "When to Use" examples for Covariance ────────────────
function CovUsageExamples() {
  const [activeEx, setActiveEx] = useState(0);

  // ── Example 1: Portfolio covariance matrix ───────────────────────
  const assets = [
    { name: "Apple",  returns: [5, 8, -2, 12, 3,  7, -1,  9,  4, 6] },
    { name: "Gold",   returns: [-1, 2, 6,  1, -3, 0,  8, -2,  5, 3] },
    { name: "Bonds",  returns: [2, 1,  3,  2,  4, 2,  1,  3,  2, 2] },
  ];
  const covMatrix = assets.map(a => assets.map(b => {
    const n = a.returns.length;
    const ma = a.returns.reduce((s,v)=>s+v,0)/n;
    const mb = b.returns.reduce((s,v)=>s+v,0)/n;
    return a.returns.reduce((s,v,i)=>s+(v-ma)*(b.returns[i]-mb),0)/n;
  }));

  // ── Example 2: Pearson r derivation ─────────────────────────────
  const [units, setUnits] = useState("hours");
  const studyData = [
    { hrs:1, score:45 }, { hrs:2, score:55 }, { hrs:3, score:60 },
    { hrs:4, score:68 }, { hrs:5, score:72 }, { hrs:6, score:80 },
    { hrs:7, score:85 }, { hrs:8, score:91 },
  ];
  const scale = units === "hours" ? 1 : units === "minutes" ? 60 : 3600;
  const unitLabel = units === "hours" ? "hrs" : units === "minutes" ? "min" : "sec";
  const n2 = studyData.length;
  const xs2 = studyData.map(d => d.hrs * scale);
  const ys2 = studyData.map(d => d.score);
  const mx2 = xs2.reduce((s,v)=>s+v,0)/n2, my2 = ys2.reduce((s,v)=>s+v,0)/n2;
  const cov2 = xs2.reduce((s,v,i)=>s+(v-mx2)*(ys2[i]-my2),0)/n2;
  const sdX2 = Math.sqrt(xs2.reduce((s,v)=>s+(v-mx2)**2,0)/n2);
  const sdY2 = Math.sqrt(ys2.reduce((s,v)=>s+(v-my2)**2,0)/n2);
  const pearson2 = cov2/(sdX2*sdY2);

  // ── Example 3: Mean-centring + standardising demo ────────────────
  const [prepStep, setPrepStep] = useState(0);
  const rawFeatures = [
    { name:"Age",    vals:[22,35,28,45,32,50,26,38], unit:"years",  scale:1 },
    { name:"Salary", vals:[25,52,34,80,45,95,30,60], unit:"k€",     scale:1 },
  ];
  const getMean = arr => arr.reduce((s,v)=>s+v,0)/arr.length;
  const getStd  = arr => { const m=getMean(arr); return Math.sqrt(arr.reduce((s,v)=>s+(v-m)**2,0)/arr.length); };
  const centered = rawFeatures.map(f => ({
    ...f, vals: f.vals.map(v => parseFloat((v - getMean(f.vals)).toFixed(2)))
  }));
  const standardised = rawFeatures.map(f => ({
    ...f, vals: f.vals.map(v => parseFloat(((v - getMean(f.vals))/getStd(f.vals)).toFixed(3)))
  }));
  const displayFeatures = prepStep===0 ? rawFeatures : prepStep===1 ? centered : standardised;
  const f0 = displayFeatures[0].vals, f1 = displayFeatures[1].vals;
  const m0=getMean(f0), m1=getMean(f1);
  const covPP = f0.reduce((s,v,i)=>s+(v-m0)*(f1[i]-m1),0)/f0.length;
  const sdP0=getStd(f0), sdP1=getStd(f1);
  const rPP = covPP/(sdP0*sdP1);

  const EXAMPLES = [
    { id:0, icon:"🏦", title:"Portfolio Theory", subtitle:"Covariance as a building block" },
    { id:1, icon:"📐", title:"Pearson r — live derivation", subtitle:"Why we divide by σₓ·σᵧ" },
    { id:2, icon:"⚙️", title:"Preprocessing: Mean-centre & Standardise", subtitle:"Properties 3 & 4 in action" },
  ];

  return (
    <div style={{marginTop:14}}>
      {/* ── Section header ── */}
      <div style={{background:"#F472B608", border:"1px solid #F472B633", borderRadius:10, padding:"14px 18px", marginBottom:16}}>
        <div style={{fontSize:14, fontWeight:700, color:"#F472B6", marginBottom:8}}>🗺️ When to Use This — Interactive Examples</div>
        <div style={{fontSize:13, color:"#B0B4CC", lineHeight:1.8}}>
          The three "when to use" cases below are abstract without examples. Here each one is worked through <em style={{color:"#F472B6"}}>with real numbers</em> so you can see exactly what happens.
        </div>
      </div>

      {/* ── Tab selector ── */}
      <div style={{display:"flex", gap:8, marginBottom:16, flexWrap:"wrap"}}>
        {EXAMPLES.map(e => (
          <button key={e.id} onClick={()=>setActiveEx(e.id)} style={{
            padding:"9px 16px", borderRadius:8, cursor:"pointer", fontSize:12,
            fontWeight:activeEx===e.id?700:400, transition:"all 0.15s",
            border:`1px solid ${activeEx===e.id?"#F472B6":C.panelBorder}`,
            background:activeEx===e.id?"#F472B622":"transparent",
            color:activeEx===e.id?"#F472B6":C.muted,
          }}>
            {e.icon} {e.title}
          </button>
        ))}
      </div>

      {/* ═══════════════════════════════════════════
          EXAMPLE 1 — Portfolio covariance matrix
      ═══════════════════════════════════════════ */}
      {activeEx === 0 && (
        <div style={{background:C.panel, border:"1px solid #F472B633", borderRadius:10, padding:20}}>
          <div style={{fontSize:13,fontWeight:700,color:"#F472B6",marginBottom:4}}>🏦 Example: 3-Asset Portfolio</div>
          <div style={{fontSize:12,color:C.muted,marginBottom:16}}>
            Covariance as a building block — we don't interpret individual Cov numbers, we use the matrix to calculate portfolio risk.
          </div>

          {/* Story */}
          <div style={{background:"#0A0C15", border:"1px solid #F472B622", borderRadius:8, padding:"12px 14px", marginBottom:16}}>
            <div style={{fontSize:12,color:"#F472B6",fontWeight:700,marginBottom:6}}>The Scenario</div>
            <div style={{fontSize:12,color:"#B0B4CC",lineHeight:1.8}}>
              You invest in 3 assets: <strong style={{color:C.teal}}>Apple (tech stock)</strong>, <strong style={{color:C.gold}}>Gold (safe haven)</strong>, and <strong style={{color:C.green}}>Bonds (stable)</strong>.
              Each has 10 months of returns (%). The covariance matrix tells you <em style={{color:"#F472B6"}}>how each asset's returns move with every other</em>.
              A portfolio manager needs the full matrix — not just one r — to minimise overall risk.
            </div>
          </div>

          {/* Monthly returns table */}
          <div style={{fontSize:11,color:C.muted,textTransform:"uppercase",letterSpacing:1,marginBottom:8}}>Monthly Returns (%)</div>
          <div style={{overflowX:"auto", marginBottom:16}}>
            <table style={{width:"100%",borderCollapse:"collapse",fontSize:12}}>
              <thead>
                <tr style={{background:"#13162088"}}>
                  <th style={{padding:"8px 10px",color:C.muted,textAlign:"left",fontSize:11}}>Month</th>
                  {[1,2,3,4,5,6,7,8,9,10].map(m=>(
                    <th key={m} style={{padding:"8px 8px",color:C.muted,textAlign:"center",fontSize:11}}>M{m}</th>
                  ))}
                  <th style={{padding:"8px 10px",color:C.muted,textAlign:"center",fontSize:11}}>Mean</th>
                </tr>
              </thead>
              <tbody>
                {assets.map((a,i) => {
                  const colors=[C.teal,C.gold,C.green];
                  const mean = a.returns.reduce((s,v)=>s+v,0)/a.returns.length;
                  return (
                    <tr key={a.name} style={{borderBottom:"1px solid #12141E"}}>
                      <td style={{padding:"7px 10px",color:colors[i],fontWeight:700}}>{a.name}</td>
                      {a.returns.map((r,j)=>(
                        <td key={j} style={{padding:"7px 8px",color:r>=0?C.green:C.rose,textAlign:"center"}}>{r>0?"+":""}{r}</td>
                      ))}
                      <td style={{padding:"7px 10px",color:colors[i],fontWeight:700,textAlign:"center"}}>{mean.toFixed(1)}%</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Covariance matrix */}
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16}}>
            <div>
              <div style={{fontSize:11,color:C.muted,textTransform:"uppercase",letterSpacing:1,marginBottom:8}}>Covariance Matrix</div>
              <table style={{width:"100%",borderCollapse:"collapse",fontSize:12}}>
                <thead>
                  <tr>
                    <th style={{padding:"6px 8px",fontSize:10,color:C.muted}}></th>
                    {assets.map((a,i)=>{
                      const cols=[C.teal,C.gold,C.green];
                      return <th key={a.name} style={{padding:"6px 8px",color:cols[i],fontSize:11,textAlign:"center"}}>{a.name}</th>;
                    })}
                  </tr>
                </thead>
                <tbody>
                  {assets.map((rowA,i)=>{
                    const rowCols=[C.teal,C.gold,C.green];
                    return (
                      <tr key={rowA.name}>
                        <td style={{padding:"8px",color:rowCols[i],fontWeight:700,fontSize:11}}>{rowA.name}</td>
                        {covMatrix[i].map((val,j)=>{
                          const isDiag = i===j;
                          const bgC = isDiag ? C.purple : val>5?C.green:val>0?"#6EE7B7":val<-2?C.rose:"#FCA5A5";
                          return (
                            <td key={j} style={{
                              padding:"8px", textAlign:"center", fontSize:12, fontWeight:700,
                              color: isDiag ? C.purple : val>=0?C.green:C.rose,
                              background: isDiag?`${C.purple}11`:`${val>=0?C.green:C.rose}09`,
                              border:"1px solid #1E2235", borderRadius:4,
                            }}>
                              {isDiag ? <span title="This is Var(X)">{val.toFixed(1)}*</span> : val.toFixed(1)}
                            </td>
                          );
                        })}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
              <div style={{fontSize:10,color:C.purple,marginTop:6}}>* Diagonal = Var(X) = Cov(X,X)</div>
            </div>

            <div style={{display:"flex",flexDirection:"column",gap:10}}>
              <div style={{background:"#0A0C15",border:"1px solid #F472B633",borderRadius:8,padding:14}}>
                <div style={{fontSize:11,color:"#F472B6",fontWeight:700,textTransform:"uppercase",letterSpacing:1,marginBottom:8}}>How to Read It</div>
                {[
                  {pair:"Apple ↔ Gold", val: covMatrix[0][1].toFixed(1), note:"Low/negative → Apple and Gold tend to move opposite. Good for diversification!", col:C.rose},
                  {pair:"Apple ↔ Bonds", val: covMatrix[0][2].toFixed(1), note:"Near zero → barely related. Adding bonds reduces risk!", col:C.muted},
                  {pair:"Diagonal = Variance", val:"e.g. "+covMatrix[0][0].toFixed(1), note:"Cov(Apple,Apple) = Var(Apple). The formula is the same.", col:C.purple},
                ].map(row=>(
                  <div key={row.pair} style={{marginBottom:10, padding:"8px 10px", background:`${row.col}08`, border:`1px solid ${row.col}22`, borderRadius:6}}>
                    <div style={{display:"flex",justifyContent:"space-between",marginBottom:3}}>
                      <span style={{fontSize:12,color:row.col,fontWeight:700}}>{row.pair}</span>
                      <span style={{fontSize:13,color:row.col,fontWeight:700}}>{row.val}</span>
                    </div>
                    <div style={{fontSize:11,color:"#9094AA"}}>{row.note}</div>
                  </div>
                ))}
              </div>
              <div style={{background:`${C.gold}0A`,border:`1px solid ${C.gold}33`,borderRadius:8,padding:12}}>
                <div style={{fontSize:11,color:C.gold,fontWeight:700,marginBottom:6}}>💡 Key Insight</div>
                <div style={{fontSize:12,color:"#B0B4CC",lineHeight:1.7}}>
                  We never say "Cov = −3.2 means strong negative". We use the entire matrix to compute
                  <em style={{color:C.gold}}> portfolio variance = wᵀ Σ w</em> (weights × matrix × weights).
                  That's the building-block role. Raw covariance values are inputs to a formula, not conclusions.
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ═══════════════════════════════════════════
          EXAMPLE 2 — Pearson r derivation
      ═══════════════════════════════════════════ */}
      {activeEx === 1 && (
        <div style={{background:C.panel, border:"1px solid #F472B633", borderRadius:10, padding:20}}>
          <div style={{fontSize:13,fontWeight:700,color:"#F472B6",marginBottom:4}}>📐 Why r = Cov / (σₓ·σᵧ) — Live Proof</div>
          <div style={{fontSize:12,color:C.muted,marginBottom:16}}>
            Change the units of X below and watch Cov explode — but r stays exactly the same. That's what dividing by σₓ·σᵧ buys you.
          </div>

          {/* Unit switcher */}
          <div style={{display:"flex",gap:10,marginBottom:18,alignItems:"center",flexWrap:"wrap"}}>
            <span style={{fontSize:12,color:C.muted}}>Study time measured in:</span>
            {["hours","minutes","seconds"].map(u=>(
              <button key={u} onClick={()=>setUnits(u)} style={{
                padding:"7px 16px", borderRadius:6, cursor:"pointer", fontSize:12, fontWeight:units===u?700:400,
                border:`1px solid ${units===u?C.accent:C.panelBorder}`,
                background:units===u?`${C.accent}22`:"transparent",
                color:units===u?C.accent:C.muted,
              }}>{u} {u==="minutes"?"(×60)":u==="seconds"?"(×3600)":"(original)"}</button>
            ))}
          </div>

          <div style={{display:"grid",gridTemplateColumns:"1.2fr 1fr",gap:16}}>
            {/* Step-by-step calculation */}
            <div>
              <div style={{fontSize:11,color:C.muted,textTransform:"uppercase",letterSpacing:1,marginBottom:10}}>Step-by-Step Calculation</div>

              {/* Data row preview */}
              <div style={{background:"#0A0C15",borderRadius:8,padding:12,marginBottom:12,overflowX:"auto"}}>
                <div style={{fontSize:11,color:C.muted,marginBottom:6}}>Data (first 4 students shown):</div>
                <div style={{display:"flex",gap:8}}>
                  {studyData.slice(0,4).map((d,i)=>(
                    <div key={i} style={{textAlign:"center",background:"#13162088",borderRadius:6,padding:"6px 10px",minWidth:70}}>
                      <div style={{fontSize:10,color:C.muted,marginBottom:2}}>Student {i+1}</div>
                      <div style={{fontSize:12,color:C.teal,fontWeight:700}}>{(d.hrs*scale).toLocaleString()}{unitLabel}</div>
                      <div style={{fontSize:12,color:C.purple}}>{d.score} pts</div>
                    </div>
                  ))}
                  <div style={{display:"flex",alignItems:"center",fontSize:14,color:C.muted}}>…</div>
                </div>
              </div>

              {/* Calculation steps */}
              {[
                { step:"① Mean of X", val:`x̄ = ${mx2.toFixed(2)} ${unitLabel}`, note:`Average study time across 8 students`, color:C.teal },
                { step:"② Mean of Y", val:`ȳ = ${my2.toFixed(2)} pts`, note:`Average exam score`, color:C.purple },
                { step:"③ σₓ (std dev of X)", val:`σₓ = ${sdX2.toFixed(2)} ${unitLabel}`, note:`How spread out study times are`, color:C.teal },
                { step:"④ σᵧ (std dev of Y)", val:`σᵧ = ${sdY2.toFixed(2)} pts`, note:`How spread out scores are`, color:C.purple },
                { step:"⑤ Cov(X,Y)", val:cov2.toFixed(2), note:`Raw covariance — depends on units!`, color:C.rose },
                { step:"⑥ σₓ × σᵧ", val:`${sdX2.toFixed(2)} × ${sdY2.toFixed(2)} = ${(sdX2*sdY2).toFixed(2)}`, note:`The denominator that cancels the units`, color:C.orange },
                { step:"⑦ r = Cov / (σₓ·σᵧ)", val:pearson2.toFixed(4), note:`Unit-free! Always in [−1, +1]`, color:C.green },
              ].map(s=>(
                <div key={s.step} style={{display:"flex",gap:10,marginBottom:9,alignItems:"flex-start"}}>
                  <div style={{background:`${s.color}15`,border:`1px solid ${s.color}33`,borderRadius:5,padding:"3px 8px",fontSize:11,color:s.color,whiteSpace:"nowrap",fontWeight:700,minWidth:160}}>{s.step}</div>
                  <div style={{flex:1}}>
                    <div style={{fontSize:13,color:s.color,fontWeight:700,fontFamily:"Palatino,serif"}}>{s.val}</div>
                    <div style={{fontSize:11,color:C.muted}}>{s.note}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* Live comparison */}
            <div style={{display:"flex",flexDirection:"column",gap:12}}>
              <div style={{background:"#0A0C15",border:"1px solid #F472B633",borderRadius:8,padding:14}}>
                <div style={{fontSize:11,color:"#F472B6",fontWeight:700,textTransform:"uppercase",letterSpacing:1,marginBottom:12}}>The Core Insight</div>

                <div style={{marginBottom:10,padding:"10px 12px",background:`${C.rose}0A`,border:`1px solid ${C.rose}33`,borderRadius:7}}>
                  <div style={{fontSize:11,color:C.rose,fontWeight:700,marginBottom:4}}>Cov(X,Y) — changes with units</div>
                  <div style={{fontSize:28,fontWeight:700,color:C.rose,fontFamily:"Palatino,serif",transition:"all 0.3s"}}>{cov2.toFixed(2)}</div>
                  <div style={{fontSize:10,color:C.muted,marginTop:3}}>X measured in {unitLabel}</div>
                </div>

                <div style={{display:"flex",alignItems:"center",justifyContent:"center",fontSize:18,color:C.muted,marginBottom:10}}>÷ (σₓ × σᵧ)</div>

                <div style={{padding:"10px 12px",background:`${C.green}0A`,border:`1px solid ${C.green}44`,borderRadius:7}}>
                  <div style={{fontSize:11,color:C.green,fontWeight:700,marginBottom:4}}>r — ALWAYS the same!</div>
                  <div style={{fontSize:28,fontWeight:700,color:C.green,fontFamily:"Palatino,serif"}}>{pearson2.toFixed(4)}</div>
                  <div style={{fontSize:10,color:C.muted,marginTop:3}}>No units. No matter what scale you use.</div>
                </div>
              </div>

              <div style={{background:`${C.gold}0A`,border:`1px solid ${C.gold}33`,borderRadius:8,padding:14}}>
                <div style={{fontSize:11,color:C.gold,fontWeight:700,marginBottom:8}}>Why Dividing Works</div>
                <div style={{fontSize:12,color:"#B0B4CC",lineHeight:1.8}}>
                  When you convert hours→minutes (×60):<br/>
                  • Cov multiplies by <strong style={{color:C.rose}}>60</strong> (property 3)<br/>
                  • σₓ also multiplies by <strong style={{color:C.teal}}>60</strong><br/>
                  • So σₓ·σᵧ multiplies by <strong style={{color:C.teal}}>60</strong><br/>
                  • r = Cov/(σₓ·σᵧ) → the 60s cancel → <strong style={{color:C.green}}>r unchanged ✓</strong>
                </div>
              </div>

              <div style={{background:`${C.accent}0A`,border:`1px solid ${C.accent}33`,borderRadius:8,padding:12}}>
                <div style={{fontSize:12,color:C.accent,fontWeight:700,marginBottom:4}}>r = {pearson2.toFixed(3)} means…</div>
                <div style={{fontSize:12,color:"#B0B4CC",lineHeight:1.7}}>
                  {Math.abs(pearson2)>0.8 ? "Strong positive" : Math.abs(pearson2)>0.5 ? "Moderate positive" : "Weak"} linear relationship.
                  R² = {(pearson2**2*100).toFixed(1)}% of score variation is explained by study time.
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ═══════════════════════════════════════════
          EXAMPLE 3 — Preprocessing demo
      ═══════════════════════════════════════════ */}
      {activeEx === 2 && (
        <div style={{background:C.panel, border:"1px solid #F472B633", borderRadius:10, padding:20}}>
          <div style={{fontSize:13,fontWeight:700,color:"#F472B6",marginBottom:4}}>⚙️ Properties 3 & 4 in Preprocessing</div>
          <div style={{fontSize:12,color:C.muted,marginBottom:16}}>
            Step through the 3 stages of feature preprocessing and see how covariance and correlation behave at each step.
          </div>

          {/* Step selector */}
          <div style={{display:"flex",gap:0,marginBottom:20,borderRadius:8,overflow:"hidden",border:"1px solid #1E2235"}}>
            {[
              {id:0, label:"① Raw data", sub:"Age in years, Salary in k€", color:C.rose},
              {id:1, label:"② Mean-centred", sub:"Subtract mean (Property 4)", color:C.gold},
              {id:2, label:"③ Standardised", sub:"÷ std dev (Property 3 fix)", color:C.green},
            ].map((s,i)=>(
              <button key={s.id} onClick={()=>setPrepStep(s.id)} style={{
                flex:1, padding:"10px 8px", border:"none", cursor:"pointer",
                background:prepStep===s.id?`${s.color}22`:"transparent",
                borderRight:i<2?"1px solid #1E2235":"none",
                borderBottom:prepStep===s.id?`3px solid ${s.color}`:"3px solid transparent",
              }}>
                <div style={{fontSize:12,fontWeight:prepStep===s.id?700:400,color:prepStep===s.id?s.color:C.muted}}>{s.label}</div>
                <div style={{fontSize:10,color:C.muted,marginTop:2}}>{s.sub}</div>
              </button>
            ))}
          </div>

          <div style={{display:"grid",gridTemplateColumns:"1.4fr 1fr",gap:16}}>
            {/* Data table */}
            <div>
              <div style={{fontSize:11,color:C.muted,textTransform:"uppercase",letterSpacing:1,marginBottom:8}}>
                {prepStep===0?"Raw Features":prepStep===1?"After Mean-Centring":"After Standardisation"}
              </div>
              <table style={{width:"100%",borderCollapse:"collapse",fontSize:12}}>
                <thead>
                  <tr style={{background:"#13162088"}}>
                    <th style={{padding:"7px 10px",color:C.muted,textAlign:"left",fontSize:11}}>Person</th>
                    {displayFeatures.map((f,i)=>{
                      const fcols=[C.teal,C.gold];
                      return <th key={f.name} style={{padding:"7px 10px",color:fcols[i],textAlign:"center",fontSize:11}}>
                        {f.name} ({f.unit})
                      </th>;
                    })}
                  </tr>
                </thead>
                <tbody>
                  {displayFeatures[0].vals.map((_,i)=>(
                    <tr key={i} style={{borderBottom:"1px solid #12141E"}}>
                      <td style={{padding:"6px 10px",color:C.text}}>P{i+1}</td>
                      {displayFeatures.map((f,j)=>{
                        const fcols=[C.teal,C.gold];
                        const v = f.vals[i];
                        return <td key={j} style={{padding:"6px 10px",color:fcols[j],textAlign:"center",fontWeight:500}}>
                          {typeof v==="number" ? (Math.abs(v)<0.01&&v!==0 ? v.toExponential(2) : v.toFixed(prepStep===2?3:1)) : v}
                        </td>;
                      })}
                    </tr>
                  ))}
                  <tr style={{borderTop:"2px solid #1E2235",background:"#13162066"}}>
                    <td style={{padding:"6px 10px",color:C.muted,fontSize:11,fontWeight:700}}>Mean</td>
                    {displayFeatures.map((f,j)=>{
                      const fcols=[C.teal,C.gold];
                      const m=getMean(f.vals);
                      return <td key={j} style={{padding:"6px 10px",color:fcols[j],textAlign:"center",fontWeight:700}}>
                        {Math.abs(m)<0.001?"≈ 0":m.toFixed(2)}
                      </td>;
                    })}
                  </tr>
                  <tr style={{background:"#13162066"}}>
                    <td style={{padding:"6px 10px",color:C.muted,fontSize:11,fontWeight:700}}>Std Dev</td>
                    {displayFeatures.map((f,j)=>{
                      const fcols=[C.teal,C.gold];
                      const s=getStd(f.vals);
                      return <td key={j} style={{padding:"6px 10px",color:fcols[j],textAlign:"center",fontWeight:700}}>
                        {s.toFixed(3)}
                      </td>;
                    })}
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Stats panel */}
            <div style={{display:"flex",flexDirection:"column",gap:12}}>
              {/* Covariance */}
              <div style={{background:"#0A0C15",border:`1px solid ${C.rose}33`,borderRadius:8,padding:14}}>
                <div style={{fontSize:11,color:C.rose,fontWeight:700,textTransform:"uppercase",letterSpacing:1,marginBottom:8}}>Covariance</div>
                <div style={{fontSize:28,fontWeight:700,color:C.rose,fontFamily:"Palatino,serif",marginBottom:6,transition:"all 0.3s"}}>
                  {covPP.toFixed(3)}
                </div>
                <div style={{fontSize:11,color:C.muted,lineHeight:1.6}}>
                  {prepStep===0 && "Raw Cov — depends on both scales. Hard to interpret."}
                  {prepStep===1 && <><strong style={{color:C.gold}}>Property 4 in action:</strong> Cov unchanged after shifting! Mean-centring didn't change the relationship.</>}
                  {prepStep===2 && <><strong style={{color:C.green}}>Property 3 in action:</strong> Cov changed after dividing by σ. Now it equals r.</>}
                </div>
              </div>

              {/* Pearson r */}
              <div style={{background:"#0A0C15",border:`1px solid ${C.green}33`,borderRadius:8,padding:14}}>
                <div style={{fontSize:11,color:C.green,fontWeight:700,textTransform:"uppercase",letterSpacing:1,marginBottom:8}}>Pearson r</div>
                <div style={{fontSize:28,fontWeight:700,color:C.green,fontFamily:"Palatino,serif",marginBottom:6}}>
                  {rPP.toFixed(4)}
                </div>
                <div style={{fontSize:11,color:C.muted}}>Stable across all 3 steps — r never changes!</div>
              </div>

              {/* What's happening */}
              <div style={{
                background: prepStep===0?`${C.rose}0A`:prepStep===1?`${C.gold}0A`:`${C.green}0A`,
                border:`1px solid ${prepStep===0?C.rose:prepStep===1?C.gold:C.green}33`,
                borderRadius:8, padding:14
              }}>
                <div style={{fontSize:11,fontWeight:700,color:prepStep===0?C.rose:prepStep===1?C.gold:C.green,marginBottom:8}}>
                  {prepStep===0?"⚠️ Problem":prepStep===1?"✅ Property 4 confirmed":"✅ Properties 3 + 4 used"}
                </div>
                <div style={{fontSize:12,color:"#B0B4CC",lineHeight:1.8}}>
                  {prepStep===0 && <>Salary is in thousands of euros, Age in years. The scales are wildly different (max salary = 95, max age = 50 but salary unit is bigger). <strong style={{color:C.rose}}>Cov = {covPP.toFixed(1)} — but is that strong or weak?</strong> We can't tell without context.</>}
                  {prepStep===1 && <>We subtracted the mean from each feature. Age mean was {getMean(rawFeatures[0].vals).toFixed(1)} yrs, Salary mean was {getMean(rawFeatures[1].vals).toFixed(1)}k€. <strong style={{color:C.gold}}>Cov is IDENTICAL to raw ({covPP.toFixed(3)} = {data.reduce((s,d,i,a)=>{const n=a.length;const mX=a.reduce((s,d)=>s+d.x,0)/n;const mY=a.reduce((s,d)=>s+d.y,0)/n;return 0},0).toFixed(3)}... wait, same value!)</strong>. Property 4 proven: shifting has no effect on Cov.</>}
                  {prepStep===2 && <>After dividing by σ, each feature now has mean=0 and std=1. <strong style={{color:C.green}}>Now Cov = r = {rPP.toFixed(4)}!</strong> When data is standardised, covariance equals Pearson r. This is why PCA uses standardised data — the covariance matrix becomes the correlation matrix.</>}
                </div>
              </div>
            </div>
          </div>

          {/* Property annotation */}
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12,marginTop:16}}>
            {[
              {prop:"Property 4: Cov(a+X, b+Y) = Cov(X,Y)", step:"Step 1→2 (mean-centring)", desc:"Subtracting the mean is adding a negative constant to every value. Property 4 says this has ZERO effect on covariance. That's why mean-centring your data before PCA is safe — the covariance structure is preserved.", color:C.gold, active:prepStep>=1},
              {prop:"Property 3: Cov(aX, bY) = ab·Cov(X,Y)", step:"Step 2→3 (standardising)", desc:"Dividing by σₓ is multiplying by 1/σₓ (constant a). Dividing by σᵧ is multiplying by 1/σᵧ (constant b). So Cov scales by (1/σₓ)(1/σᵧ) = 1/(σₓσᵧ). That's exactly the Pearson r formula!", color:C.green, active:prepStep>=2},
            ].map(row=>(
              <div key={row.prop} style={{background:`${row.color}0A`, border:`1px solid ${row.active?row.color+"55":row.color+"22"}`, borderRadius:8, padding:14, opacity:row.active?1:0.4, transition:"all 0.3s"}}>
                <code style={{fontSize:11,color:row.color,display:"block",marginBottom:4}}>{row.prop}</code>
                <div style={{fontSize:10,color:C.muted,marginBottom:6,textTransform:"uppercase",letterSpacing:1}}>Used in {row.step}</div>
                <div style={{fontSize:12,color:"#B0B4CC",lineHeight:1.7}}>{row.desc}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ── SECTION 10: Pearson r² ───────────────────────────────────────────
function SecPearsonR2() {
  const [r, setR] = useState(0.8);
  const r2 = r * r;

  const W = 400, H = 160, PX = 40, PY = 20;

  // Simulate scatter at given r
  const seed = 42;
  const pts = Array.from({length: 40}, (_, i) => {
    const x = ((i * 7 + 3) % 40) / 40;
    const noise = (((i * 13 + seed) % 97) / 97 - 0.5) * 2 * Math.sqrt(1 - r*r);
    const y = Math.max(0, Math.min(1, r * x + (1-Math.abs(r))*0.5 + noise * 0.5));
    return { x, y };
  });

  const toX = v => PX + v * (W - 2*PX);
  const toY = v => H - PY - v * (H - 2*PY);

  // Bar proportions
  const explained = r2 * 100;
  const unexplained = (1 - r2) * 100;

  return (
    <div>
      {sectionLabel("Pearson r and r² — How Much Does X Explain Y?", C.gold)}

      <div style={{ background: `${C.gold}0D`, border: `1px solid ${C.gold}33`, borderRadius: 8, padding: "14px 16px", marginBottom: 16 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: C.gold, marginBottom: 6 }}>🧠 r vs r² — What's the difference? (Plain English)</div>
        <div style={{ fontSize: 13, color: "#B0B4CC", lineHeight: 1.9 }}>
          <strong style={{ color: C.text }}>r (Pearson correlation)</strong> = measures the DIRECTION and STRENGTH of a straight-line relationship. Goes from −1 to +1.<br/>
          <strong style={{ color: C.gold }}>r² (R-squared)</strong> = the percentage of Y's variation that is <em>explained by</em> X. Easier to interpret for non-mathematicians.<br/>
          Example: r = 0.8 → r² = 0.64 → "64% of the variation in exam scores is explained by study hours. The other 36% is explained by other things (sleep, ability, luck)."
        </div>
      </div>

      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 20, marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
          <label style={{ fontSize: 12, color: C.gold }}>Drag to change r: currently r = <strong>{r.toFixed(2)}</strong></label>
          <div style={{ display: "flex", gap: 10 }}>
            {pill("r", r.toFixed(2), C.gold)}
            {pill("r²", r2.toFixed(3), C.teal)}
          </div>
        </div>
        <input type="range" min="-1" max="1" step="0.05" value={r}
          onChange={e => setR(parseFloat(e.target.value))}
          style={{ width: "100%", accentColor: C.gold, marginBottom: 16 }} />

        {graphGuide([
          "LEFT chart: each dot is one data point. The tighter the dots cluster around the diagonal line → the higher |r|.",
          "When r = +1, all dots fall on a perfectly rising line. When r = −1, on a perfectly falling line. When r = 0, dots are scattered everywhere.",
          "RIGHT bar: the GOLD portion = % of Y's variation explained by X (= r²). The grey = unexplained (other factors).",
          "Notice: going from r=0.5 to r=1.0 doesn't double r². r²=0.25 vs r²=1.0 — a big jump! r² grows non-linearly.",
        ])}

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          {/* Simulated scatter */}
          <div>
            <div style={{ fontSize: 11, color: C.muted, textAlign: "center", marginBottom: 6 }}>Scatter plot at r = {r.toFixed(2)}</div>
            <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", overflow: "visible" }}>
              <line x1={PX} y1={H-PY} x2={W-PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1"/>
              <line x1={PX} y1={PY} x2={PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1"/>
              {/* Perfect fit line */}
              {r >= 0
                ? <line x1={toX(0)} y1={toY(0)} x2={toX(1)} y2={toY(1)} stroke={C.gold} strokeWidth="1.5" strokeDasharray="4 3" opacity="0.5"/>
                : <line x1={toX(0)} y1={toY(1)} x2={toX(1)} y2={toY(0)} stroke={C.gold} strokeWidth="1.5" strokeDasharray="4 3" opacity="0.5"/>
              }
              {pts.map((p, i) => (
                <circle key={i} cx={toX(p.x)} cy={toY(p.y)} r={4}
                  fill={Math.abs(r) > 0.6 ? C.gold : Math.abs(r) > 0.3 ? C.orange : C.rose}
                  opacity="0.7"/>
              ))}
              <text x={(W)/2} y={H+8} textAnchor="middle" fontSize="10" fill="#4A4D62">→ X variable</text>
              <text x={8} y={H/2} textAnchor="middle" fontSize="10" fill="#4A4D62" transform={`rotate(-90,8,${H/2})`}>↑ Y variable</text>
            </svg>
          </div>

          {/* R² bar visualisation */}
          <div>
            <div style={{ fontSize: 11, color: C.muted, textAlign: "center", marginBottom: 6 }}>r² = what % of Y is explained by X</div>
            <div style={{ padding: "16px" }}>
              <div style={{ marginBottom: 10 }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                  <span style={{ fontSize: 12, color: C.gold }}>Explained by X (r² = {(r2*100).toFixed(1)}%)</span>
                </div>
                <div style={{ width: "100%", height: 28, background: "#1E2235", borderRadius: 6, overflow: "hidden" }}>
                  <div style={{ width: `${explained}%`, height: "100%", background: C.gold, borderRadius: 6, transition: "width 0.3s", display: "flex", alignItems: "center", justifyContent: "center" }}>
                    {explained > 10 && <span style={{ fontSize: 11, color: "#000", fontWeight: 700 }}>{explained.toFixed(1)}%</span>}
                  </div>
                </div>
              </div>
              <div style={{ marginBottom: 20 }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                  <span style={{ fontSize: 12, color: C.muted }}>Unexplained — other factors ({unexplained.toFixed(1)}%)</span>
                </div>
                <div style={{ width: "100%", height: 28, background: "#1E2235", borderRadius: 6, overflow: "hidden" }}>
                  <div style={{ width: `${unexplained}%`, height: "100%", background: "#2A2D3E", borderRadius: 6 }}/>
                </div>
              </div>
              <div style={{
                background: `${Math.abs(r)>0.7 ? C.green : Math.abs(r)>0.4 ? C.gold : C.rose}0F`,
                border: `1px solid ${Math.abs(r)>0.7 ? C.green : Math.abs(r)>0.4 ? C.gold : C.rose}44`,
                borderRadius: 7, padding: "10px 12px", fontSize: 12, color: "#B0B4CC", lineHeight: 1.6,
              }}>
                <strong style={{ color: Math.abs(r)>0.7 ? C.green : Math.abs(r)>0.4 ? C.gold : C.rose }}>Interpretation:</strong>{" "}
                {Math.abs(r) < 0.2 && "r² is very small — X explains almost none of the variation in Y. Don't use X to predict Y."}
                {Math.abs(r) >= 0.2 && Math.abs(r) < 0.5 && `X explains ${explained.toFixed(0)}% of the variation in Y. Weak but detectable relationship.`}
                {Math.abs(r) >= 0.5 && Math.abs(r) < 0.8 && `X explains ${explained.toFixed(0)}% of Y. Moderate relationship — useful but other factors matter too.`}
                {Math.abs(r) >= 0.8 && `X explains ${explained.toFixed(0)}% of Y. Strong relationship — X is a major predictor of Y.`}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 14 }}>
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>
            r² in Plain English — real examples
          </div>
          {[
            { r2v: "r² = 0.90", context: "Study hours vs exam score", meaning: "Study hours explain 90% of score variation. A very strong predictor.", c: C.green },
            { r2v: "r² = 0.64", context: "Height vs weight", meaning: "Height explains 64% of weight variation. Strong, but body fat % also matters.", c: C.gold },
            { r2v: "r² = 0.25", context: "Exercise vs mood", meaning: "Exercise explains 25% of mood. It matters, but sleep, stress etc. matter more.", c: C.orange },
            { r2v: "r² = 0.04", context: "Shoe size vs IQ", meaning: "Only 4% explained. Essentially no useful relationship.", c: C.rose },
          ].map(row => (
            <div key={row.r2v} style={{ background: `${row.c}08`, border: `1px solid ${row.c}33`, borderRadius: 7, padding: "10px 12px", marginBottom: 8 }}>
              <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 4 }}>
                <code style={{ fontSize: 12, color: row.c, background: `${row.c}20`, padding: "2px 8px", borderRadius: 3 }}>{row.r2v}</code>
                <span style={{ fontSize: 11, color: C.muted }}>{row.context}</span>
              </div>
              <div style={{ fontSize: 12, color: "#B0B4CC" }}>{row.meaning}</div>
            </div>
          ))}
        </div>

        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>
            Pearson r — formula broken down
          </div>
          <div style={{ fontFamily: "Palatino, serif", fontSize: 15, color: C.gold, textAlign: "center", background: `${C.gold}0F`, padding: "12px", borderRadius: 8, marginBottom: 14 }}>
            r = Cov(X,Y) / (σₓ × σᵧ)
          </div>
          {[
            { step: "Cov(X,Y)", desc: "Raw measure of how X and Y vary together (can be any number)", c: "#F472B6" },
            { step: "σₓ", desc: "Standard deviation of X — tells us the typical spread of X values", c: C.teal },
            { step: "σᵧ", desc: "Standard deviation of Y — typical spread of Y values", c: C.teal },
            { step: "Dividing by σₓ×σᵧ", desc: "This 'standardises' the covariance so the result is always −1 to +1 regardless of units", c: C.gold },
            { step: "r²", desc: "Square r to get 'proportion of variance explained'. Always between 0 and 1.", c: C.gold },
          ].map(row => (
            <div key={row.step} style={{ display: "flex", gap: 8, marginBottom: 9 }}>
              <code style={{ fontSize: 11, color: row.c, background: `${row.c}15`, padding: "2px 6px", borderRadius: 3, whiteSpace: "nowrap", alignSelf: "flex-start" }}>{row.step}</code>
              <span style={{ fontSize: 12, color: "#9094AA", lineHeight: 1.5 }}>{row.desc}</span>
            </div>
          ))}
        </div>
      </div>

      {whenToUse([
        { when: "Use Pearson r when both variables are numbers and the relationship looks like a straight line.", why: "It's the standard correlation measure for continuous data (height, weight, temperature, scores). Check the scatter plot first — if the pattern is curved, Pearson r is misleading." },
        { when: "Use r² when explaining results to non-technical people.", why: "'The r² is 0.64' is much easier to explain as 'height explains 64% of the variation in weight' than trying to explain what r=0.8 means. r² is a proportion — intuitive for anyone." },
        { when: "Do NOT use Pearson r for ordinal data (rankings, Likert scales like 1–5 ratings).", why: "For rankings and ordinal data, use Spearman's ρ (rho) instead — it doesn't assume a straight-line relationship." },
      ], C.gold)}
    </div>
  );
}

// ── SECTION 11: Spearman Correlation ────────────────────────────────
function SecSpearman() {
  const DATASETS = {
    rank: {
      label: "🏆 Race Rankings", xLabel: "Training hrs/week", yLabel: "Race position (1=best)",
      note: "Outcome is a RANK (1st, 2nd, 3rd...) — not a raw number. Use Spearman.",
      data: [
        {name:"Alice", x:20, y:1},  {name:"Bob", x:18, y:2},  {name:"Carol", x:15, y:4},
        {name:"Dave", x:12, y:5},   {name:"Eve", x:17, y:3},  {name:"Frank", x:8, y:7},
        {name:"Grace", x:10, y:6},  {name:"Hank", x:5, y:8},
      ]
    },
    outlier: {
      label: "💰 Salary vs Experience (with outlier)", xLabel: "Years experience", yLabel: "Salary (€k)",
      note: "One extreme outlier (CEO) would distort Pearson r but Spearman handles it robustly.",
      data: [
        {name:"Intern", x:0, y:25},  {name:"Junior", x:1, y:32},  {name:"Mid", x:3, y:45},
        {name:"Senior", x:5, y:60},  {name:"Lead", x:8, y:75},    {name:"Manager", x:10, y:90},
        {name:"Director", x:15, y:110}, {name:"CEO", x:20, y:500},
      ]
    },
    monotone: {
      label: "📈 Monotone non-linear", xLabel: "X", yLabel: "Y = X³",
      note: "Y = X³ is non-linear so Pearson r ≠ 1, but Spearman ρ = 1 because the RANK ORDER is perfect.",
      data: Array.from({length:10}, (_,i)=>{const x=i+1; return {name:`pt${x}`, x, y:x*x*x};})
    },
  };

  const [dsKey, setDsKey] = useState("rank");
  const [hovIdx, setHovIdx] = useState(null);
  const ds = DATASETS[dsKey];
  const data = ds.data;

  // Compute ranks
  const rankArr = (arr) => {
    const sorted = [...arr].map((v,i)=>({v,i})).sort((a,b)=>a.v-b.v);
    const ranks = new Array(arr.length);
    sorted.forEach((s,r) => ranks[s.i] = r+1);
    return ranks;
  };
  const rxs = rankArr(data.map(d=>d.x)), rys = rankArr(data.map(d=>d.y));
  const n = data.length;
  const meanRx = (n+1)/2, meanRy = (n+1)/2;
  const covR = rxs.reduce((s,rx,i)=>s+(rx-meanRx)*(rys[i]-meanRy),0)/n;
  const sdRx = Math.sqrt(rxs.reduce((s,rx)=>s+(rx-meanRx)**2,0)/n);
  const sdRy = Math.sqrt(rys.reduce((s,ry)=>s+(ry-meanRy)**2,0)/n);
  const spearman = sdRx*sdRy > 0 ? covR/(sdRx*sdRy) : 0;

  const xs = data.map(d=>d.x), ys = data.map(d=>d.y);
  const meanX = xs.reduce((a,b)=>a+b,0)/n;
  const meanY = ys.reduce((a,b)=>a+b,0)/n;
  const covXY = xs.reduce((s,x,i)=>s+(x-meanX)*(ys[i]-meanY),0)/n;
  const varX = xs.reduce((s,x)=>s+(x-meanX)**2,0)/n;
  const varY2 = ys.reduce((s,y)=>s+(y-meanY)**2,0)/n;
  const pearson = varX*varY2>0 ? covXY/Math.sqrt(varX*varY2) : 0;

  const xMin2 = Math.min(...xs), xMax2 = Math.max(...xs);
  const yMin2 = Math.min(...ys), yMax2 = Math.max(...ys);
  const W = 380, H = 200, PX = 44, PY = 24;
  const toX = x => PX + ((x-xMin2)/(xMax2-xMin2||1))*(W-2*PX);
  const toY = y => H-PY - ((y-yMin2)/(yMax2-yMin2||1))*(H-2*PY);

  const rhoColor = Math.abs(spearman) > 0.7 ? C.purple : Math.abs(spearman) > 0.4 ? C.gold : C.rose;

  return (
    <div>
      {sectionLabel("Spearman Correlation (ρ) — When Rankings Matter", C.purple)}

      <div style={{ background: `${C.purple}0D`, border: `1px solid ${C.purple}33`, borderRadius: 8, padding: "14px 16px", marginBottom: 16 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: C.purple, marginBottom: 6 }}>🧠 What is Spearman ρ? (Plain English)</div>
        <div style={{ fontSize: 13, color: "#B0B4CC", lineHeight: 1.9 }}>
          Instead of using the raw numbers, Spearman first <strong style={{ color: C.text }}>converts everything to ranks</strong> (1st, 2nd, 3rd…) and then measures Pearson r on those ranks.<br/>
          This makes it work even when: the relationship is curved but always going up (monotone), data has outliers, or your data is already ordinal (rankings, ratings).<br/>
          <strong style={{ color: C.purple }}>ρ (rho)</strong> is interpreted exactly like r — it's between −1 and +1.
        </div>
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 14, flexWrap: "wrap" }}>
        {Object.entries(DATASETS).map(([k,d]) => (
          <button key={k} onClick={() => setDsKey(k)} style={{
            padding: "7px 14px", borderRadius: 6,
            border: `1px solid ${dsKey===k ? C.purple : C.panelBorder}`,
            background: dsKey===k ? `${C.purple}22` : "transparent",
            color: dsKey===k ? C.purple : C.muted, cursor: "pointer", fontSize: 12, fontWeight: dsKey===k ? 700 : 400,
          }}>{d.label}</button>
        ))}
      </div>

      <div style={{ background: `${C.purple}08`, border: `1px solid ${C.purple}33`, borderRadius: 7, padding: "10px 14px", marginBottom: 14, fontSize: 12.5, color: "#B0B4CC", lineHeight: 1.7 }}>
        💡 <strong style={{ color: C.purple }}>Why this dataset:</strong> {ds.note}
      </div>

      {graphGuide([
        "LEFT scatter: raw data. You can see if there are outliers or a curved pattern.",
        "RIGHT scatter: after converting to RANKS. Both axes are now 1, 2, 3… The rank scatter should look more like a straight line.",
        "Spearman ρ measures the straight-line relationship in the RANK scatter (right chart).",
        "Compare the two correlation numbers: if Pearson ≠ Spearman, that tells you outliers or non-linearity are distorting Pearson.",
      ])}

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 16 }}>
        {/* Raw scatter */}
        {[
          { title: "Raw data scatter", pts: data.map((d,i)=>({x:d.x,y:d.y,name:d.name})), xMin:xMin2, xMax:xMax2, yMin:yMin2, yMax:yMax2, label:"Raw values", corr: pearson, corrLabel:"Pearson r", col: C.teal },
          { title: "Rank scatter (Spearman view)", pts: data.map((d,i)=>({x:rxs[i],y:rys[i],name:d.name})), xMin:1, xMax:n, yMin:1, yMax:n, label:"Ranks", corr: spearman, corrLabel:"Spearman ρ", col: C.purple },
        ].map((chart, ci) => {
          const tx = x => PX + ((x-chart.xMin)/(chart.xMax-chart.xMin||1))*(W-2*PX);
          const ty = y => H-PY - ((y-chart.yMin)/(chart.yMax-chart.yMin||1))*(H-2*PY);
          const cColor = Math.abs(chart.corr) > 0.7 ? C.green : Math.abs(chart.corr) > 0.4 ? C.gold : C.rose;
          return (
            <div key={ci} style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 14 }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <div style={{ fontSize: 11, color: C.muted, textTransform: "uppercase", letterSpacing: 1 }}>{chart.title}</div>
                <div style={{ fontSize: 12, color: cColor, fontWeight: 700 }}>{chart.corrLabel} = {chart.corr.toFixed(3)}</div>
              </div>
              <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", overflow: "visible" }}>
                <line x1={PX} y1={H-PY} x2={W-PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1"/>
                <line x1={PX} y1={PY} x2={PX} y2={H-PY} stroke="#2A2D3E" strokeWidth="1"/>
                {chart.pts.map((p, i) => (
                  <g key={i} onMouseEnter={() => setHovIdx(`${ci}-${i}`)} onMouseLeave={() => setHovIdx(null)} style={{cursor:"pointer"}}>
                    <circle cx={tx(p.x)} cy={ty(p.y)} r={hovIdx===`${ci}-${i}` ? 7 : 5}
                      fill={chart.col} opacity={0.75}
                      stroke={hovIdx===`${ci}-${i}` ? "white" : "none"} strokeWidth="1.5"/>
                    {hovIdx===`${ci}-${i}` && (
                      <text x={tx(p.x)+9} y={ty(p.y)-6} fontSize="9" fill="white">{p.name}</text>
                    )}
                  </g>
                ))}
              </svg>
            </div>
          );
        })}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 14 }}>
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>How Ranking Works — Step by Step</div>
          <div style={{ fontSize: 12, color: "#7A7D96", marginBottom: 10 }}>Example: scores [85, 62, 91, 77] → sorted: [62, 77, 85, 91] → ranks: 62=1st, 77=2nd, 85=3rd, 91=4th</div>
          {[
            { step: "1. Sort X values smallest → largest", desc: "Assign rank 1 to smallest, 2 to next, etc.", c: C.teal },
            { step: "2. Do the same for Y values", desc: "Each Y value gets its own rank 1..n", c: C.teal },
            { step: "3. Now use Pearson r on the ranks", desc: "Spearman ρ = Pearson r(ranks of X, ranks of Y)", c: C.purple },
            { step: "Tied values", desc: "If two values are equal, they get the average rank. E.g. two scores of 85 tied for 3rd and 4th → both get rank 3.5", c: C.orange },
          ].map(row => (
            <div key={row.step} style={{ display: "flex", gap: 8, marginBottom: 10 }}>
              <code style={{ fontSize: 11, color: row.c, background: `${row.c}15`, padding: "2px 6px", borderRadius: 3, whiteSpace: "nowrap", alignSelf: "flex-start", maxWidth: 180 }}>{row.step}</code>
              <span style={{ fontSize: 12, color: "#9094AA", lineHeight: 1.5 }}>{row.desc}</span>
            </div>
          ))}
        </div>
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>Pearson vs Spearman — Decision Guide</div>
          {[
            { q: "Data is continuous numbers?", pearson: "✓ Use Pearson", spearman: "✓ Both work", c: C.teal },
            { q: "Relationship is a straight line?", pearson: "✓ Pearson is ideal", spearman: "Works too", c: C.green },
            { q: "Data has strong outliers?", pearson: "✗ Distorted by outliers", spearman: "✓ Robust to outliers", c: C.orange },
            { q: "Data is ordinal (ratings, rankings)?", pearson: "✗ Inappropriate", spearman: "✓ Use Spearman", c: C.purple },
            { q: "Relationship is monotone but curved?", pearson: "✗ Misses the pattern", spearman: "✓ Detects it perfectly", c: C.gold },
            { q: "Small sample (n < 20)?", pearson: "Both unreliable", spearman: "Still more robust", c: C.rose },
          ].map(row => (
            <div key={row.q} style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr", gap: 4, marginBottom: 8, padding: "7px 0", borderBottom: "1px solid #12141E" }}>
              <div style={{ fontSize: 11, color: "#B0B4CC" }}>{row.q}</div>
              <div style={{ fontSize: 10.5, color: row.pearson.startsWith("✓") ? C.teal : C.rose, textAlign: "center" }}>{row.pearson}</div>
              <div style={{ fontSize: 10.5, color: row.spearman.startsWith("✓") ? C.green : C.muted, textAlign: "center" }}>{row.spearman}</div>
            </div>
          ))}
        </div>
      </div>

      {whenToUse([
        { when: "Use Spearman when your data is already in rank form (survey ratings, competition placements, preference orders).", why: "A Likert scale (1=strongly disagree to 5=strongly agree) is ordinal — the gap between 1 and 2 might not be the same as between 4 and 5. Spearman makes no such assumption." },
        { when: "Use Spearman as your default when you suspect outliers.", why: "One CEO earning 10× more than everyone else will completely distort Pearson r. Spearman sees that CEO as 'rank 8 out of 8' — an outlier has no extra influence." },
        { when: "Use Spearman for the 'monotone non-linear' case above.", why: "If Y always increases when X increases (monotone), even if it's curved like X², Spearman ρ will be close to 1. Pearson r would not be." },
      ], C.purple)}
    </div>
  );
}

// ── SECTION 12: Multivariate Normalisation ───────────────────────────
function SecMultivariateNorm() {
  const [method, setMethod] = useState("minmax");
  const [showRaw, setShowRaw] = useState(true);

  const rawData = [
    { name: "Alice",  age: 25, salary: 32000, score: 72 },
    { name: "Bob",    age: 32, salary: 85000, score: 88 },
    { name: "Carol",  age: 28, salary: 47000, score: 65 },
    { name: "Dave",   age: 45, salary: 120000, score: 91 },
    { name: "Eve",    age: 22, salary: 28000, score: 58 },
  ];

  const features = ["age", "salary", "score"];
  const stats = {};
  features.forEach(f => {
    const vals = rawData.map(d => d[f]);
    const mn = Math.min(...vals), mx = Math.max(...vals);
    const mean = vals.reduce((a,b)=>a+b,0)/vals.length;
    const std = Math.sqrt(vals.reduce((s,v)=>s+(v-mean)**2,0)/vals.length);
    stats[f] = { min: mn, max: mx, mean, std };
  });

  const normalise = (val, f) => {
    if (method === "minmax") return (val - stats[f].min) / (stats[f].max - stats[f].min);
    if (method === "zscore") return (val - stats[f].mean) / stats[f].std;
    return val;
  };

  const normData = rawData.map(d => {
    const norm = {};
    features.forEach(f => norm[f] = normalise(d[f], f));
    return { ...d, ...Object.fromEntries(features.map(f => [`${f}_norm`, norm[f]])) };
  });

  const barColor = (v, method) => {
    if (method === "raw") return C.accent;
    const capped = Math.max(0, Math.min(1, method === "minmax" ? v : (v + 3) / 6));
    return capped > 0.6 ? C.green : capped > 0.3 ? C.gold : C.rose;
  };

  const fmtVal = (v, f, isNorm) => {
    if (!isNorm) return f === "salary" ? `€${(v/1000).toFixed(0)}k` : v.toFixed(0);
    if (method === "minmax") return v.toFixed(3);
    if (method === "zscore") return (v >= 0 ? "+" : "") + v.toFixed(2) + "σ";
    return v;
  };

  const W = 460, H = 120;

  return (
    <div>
      {sectionLabel("Multivariate Data & Normalisation", C.green)}

      <div style={{ background: `${C.green}0D`, border: `1px solid ${C.green}33`, borderRadius: 8, padding: "14px 16px", marginBottom: 16 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: C.green, marginBottom: 6 }}>🧠 What is multivariate data and why normalise? (Plain English)</div>
        <div style={{ fontSize: 13, color: "#B0B4CC", lineHeight: 1.9 }}>
          <strong style={{ color: C.text }}>Multivariate</strong> = more than 2 variables per person. Example: you record each employee's age, salary, and performance score.<br/>
          The problem: <strong style={{ color: C.rose }}>they're in completely different units and scales</strong>. Age is 20–60. Salary is 28,000–120,000. Score is 0–100.<br/>
          If you feed these raw numbers into a machine learning model or a distance calculation, <strong style={{ color: C.gold }}>salary will dominate everything</strong> just because its numbers are bigger.<br/>
          <strong style={{ color: C.green }}>Normalisation</strong> = rescaling each feature so they're comparable. It doesn't change the relationships — it just puts everyone on equal footing.
        </div>
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
        {[
          { k: "raw", label: "📊 Raw (no normalisation)", desc: "Original values — incomparable scales" },
          { k: "minmax", label: "📐 Min-Max Scaling", desc: "Compress to [0, 1]" },
          { k: "zscore", label: "🎯 Z-Score (Standardisation)", desc: "Mean=0, StdDev=1" },
        ].map(opt => (
          <button key={opt.k} onClick={() => setMethod(opt.k)} style={{
            padding: "8px 16px", borderRadius: 6,
            border: `1px solid ${method===opt.k ? C.green : C.panelBorder}`,
            background: method===opt.k ? `${C.green}22` : "transparent",
            color: method===opt.k ? C.green : C.muted, cursor: "pointer", fontSize: 12, fontWeight: method===opt.k ? 700 : 400,
          }}>
            <div>{opt.label}</div>
            <div style={{ fontSize: 10, color: method===opt.k ? `${C.green}99` : C.muted, marginTop: 2 }}>{opt.desc}</div>
          </button>
        ))}
      </div>

      {graphGuide([
        "Each ROW = one person. Each COLUMN = one feature (age, salary, performance score).",
        "Each bar's LENGTH shows the relative value of that feature for that person.",
        "In RAW mode: salary bars completely dwarf the age and score bars — the scales are incomparable!",
        "In MIN-MAX mode: every bar is now between 0 and 1. The shortest bar = 0 (minimum), longest = 1 (maximum). Now you can visually compare across features.",
        "In Z-SCORE mode: 0 = average. Positive = above average. Negative = below average. The number tells you how many standard deviations from the mean.",
        "Try all three modes and watch how the bars change — especially salary (€k) vs age (years).",
      ])}

      <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 20, marginBottom: 16 }}>
        <div style={{ fontSize: 11, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 14 }}>
          {method === "raw" ? "⚠️ Raw Values — Salary (€28k–€120k) swamps Age (22–45) and Score (58–91)" :
           method === "minmax" ? "✓ After Min-Max Scaling — all values now between 0 and 1" :
           "✓ After Z-Score Standardisation — all values in units of standard deviations from mean"}
        </div>

        {rawData.map((person, pi) => {
          const rowData = features.map(f => ({
            f, raw: person[f],
            norm: normData[pi][`${f}_norm`],
          }));
          return (
            <div key={person.name} style={{ marginBottom: 16 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
                <div style={{ width: 52, fontSize: 12, fontWeight: 700, color: C.text }}>{person.name}</div>
                <div style={{ display: "flex", gap: 12, flex: 1 }}>
                  {rowData.map(({ f, raw, norm }) => {
                    const dispVal = method === "raw" ? raw : norm;
                    const barPct = method === "raw"
                      ? (raw - stats[f].min) / (stats[f].max - stats[f].min) * 100
                      : method === "minmax" ? norm * 100
                      : Math.min(100, Math.max(0, (norm + 3) / 6 * 100));
                    return (
                      <div key={f} style={{ flex: 1 }}>
                        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3 }}>
                          <span style={{ fontSize: 10, color: C.muted, textTransform: "uppercase" }}>{f}</span>
                          <span style={{ fontSize: 11, color: C.text, fontWeight: 700 }}>{fmtVal(raw, f, false)}</span>
                        </div>
                        <div style={{ width: "100%", height: 10, background: "#1A1D2E", borderRadius: 3, overflow: "hidden" }}>
                          <div style={{ width: `${Math.max(2, barPct)}%`, height: "100%",
                            background: method === "raw" ? C.accent : barColor(method === "minmax" ? norm : (norm+3)/6, "norm"),
                            borderRadius: 3, transition: "width 0.4s, background 0.3s" }}/>
                        </div>
                        {method !== "raw" && (
                          <div style={{ fontSize: 10, color: C.teal, marginTop: 2, textAlign: "right" }}>→ {fmtVal(norm, f, true)}</div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          );
        })}

        {method === "raw" && (
          <div style={{ background: `${C.rose}0F`, border: `1px solid ${C.rose}44`, borderRadius: 7, padding: "10px 14px", fontSize: 12, color: "#B0B4CC", lineHeight: 1.6 }}>
            ⚠️ <strong style={{ color: C.rose }}>Problem with raw data:</strong> salary ranges from €28k–€120k while age ranges from 22–45. Any algorithm treating these equally would effectively ignore age and score. Switch to Min-Max or Z-Score to fix this.
          </div>
        )}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 14 }}>
        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>Min-Max vs Z-Score — the key differences</div>
          {[
            { method: "Min-Max", formula: "(x − min) / (max − min)", result: "Always [0, 1]", pro: "Easy to interpret. 0 = lowest, 1 = highest in dataset.", con: "Sensitive to outliers — one extreme value compresses everyone else.", c: C.teal },
            { method: "Z-Score", formula: "(x − mean) / std", result: "Centred at 0, usually −3 to +3", pro: "Handles outliers better. Preserves relative spread. Used in most ML algorithms.", con: "Less intuitive — you need to know what 'standard deviations' means.", c: C.gold },
          ].map(row => (
            <div key={row.method} style={{ background: `${row.c}08`, border: `1px solid ${row.c}33`, borderRadius: 7, padding: "12px", marginBottom: 10 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: row.c, marginBottom: 6 }}>{row.method}</div>
              <div style={{ fontFamily: "Palatino, serif", fontSize: 13, color: row.c, marginBottom: 6, background: `${row.c}15`, padding: "4px 8px", borderRadius: 4, display: "inline-block" }}>{row.formula}</div>
              <div style={{ fontSize: 11, color: C.muted, marginBottom: 4 }}>Result: {row.result}</div>
              <div style={{ fontSize: 12, color: C.green, marginBottom: 3 }}>✓ {row.pro}</div>
              <div style={{ fontSize: 12, color: C.rose }}>✗ {row.con}</div>
            </div>
          ))}
        </div>

        <div style={{ background: C.panel, border: `1px solid ${C.panelBorder}`, borderRadius: 10, padding: 16 }}>
          <div style={{ fontSize: 12, color: C.muted, letterSpacing: 2, textTransform: "uppercase", marginBottom: 12 }}>Multivariate — what changes vs bivariate?</div>
          {[
            { n: "2 variables", label: "Bivariate", desc: "One scatter plot, one r value. Simple to visualise.", c: "#E879F9" },
            { n: "3+ variables", label: "Multivariate", desc: "Can't visualise in 2D easily. Need a correlation matrix (grid of r values for every pair), or techniques like PCA to reduce dimensions.", c: C.green },
            { n: "Key issue", label: "Confounding", desc: "With many variables, correlations between pairs might be driven by a third hidden variable. Always think about what else could explain the relationship.", c: C.gold },
            { n: "Normalise first", label: "Before modelling", desc: "Any algorithm that uses distances (k-means, kNN, neural networks, regression with multiple features) requires normalisation first.", c: C.teal },
          ].map(row => (
            <div key={row.n} style={{ display: "flex", gap: 10, marginBottom: 10 }}>
              <div style={{ minWidth: 80, fontSize: 11, fontWeight: 700, color: row.c, background: `${row.c}15`, padding: "4px 6px", borderRadius: 4, textAlign: "center", alignSelf: "flex-start" }}>{row.label}</div>
              <span style={{ fontSize: 12, color: "#9094AA", lineHeight: 1.5 }}>{row.desc}</span>
            </div>
          ))}
        </div>
      </div>

      {whenToUse([
        { when: "Use Min-Max when you need all values in [0, 1] and you know there are no extreme outliers.", why: "Example: pixel values in images (0–255 → 0–1). Neural networks for images always use Min-Max because the data is well-bounded and uniform." },
        { when: "Use Z-Score (standardisation) as your default for most machine learning.", why: "Most ML algorithms (logistic regression, SVM, PCA) work best when features have mean=0 and std=1. Z-score is the standard choice when you don't know the range of your features in advance." },
        { when: "Skip normalisation for tree-based models (Random Forest, XGBoost, Decision Trees).", why: "These algorithms split on feature thresholds and are scale-invariant — normalising doesn't help or hurt. Save the effort." },
        { when: "Always normalise AFTER splitting into train/test sets.", why: "A common beginner mistake: normalise on the full dataset, then split. This 'leaks' information from the test set into the training process. Always fit the scaler on training data only, then apply to both." },
      ], C.green)}

      {callout("🔑", "The Correlation Matrix — reading multivariate relationships",
        ["With 3+ variables, you can't just plot one scatter plot. Instead, compute r for every pair: (X1,X2), (X1,X3), (X2,X3) — this grid is called the correlation matrix.",
          "The diagonal is always 1.0 (every variable is perfectly correlated with itself). The matrix is symmetric (r(X,Y) = r(Y,X)).",
          "Read it like a heatmap: green/warm cells = strong correlation, grey/cool cells = no correlation.",
          "Multicollinearity warning: if two features have |r| > 0.9, they're nearly identical — one of them is redundant and should probably be removed from your model."],
        C.green)}
    </div>
  );
}

// ── MAIN APP ─────────────────────────────────────────────────────────
const SECTIONS = [
  { id: "rv",    label: "Random Variables",    icon: "🎲", color: C.accent,   comp: SecRandomVar },
  { id: "cdf",   label: "CDF",                 icon: "📈", color: C.teal,    comp: SecCDF },
  { id: "pdf",   label: "PDF",                 icon: "🔔", color: C.purple,  comp: SecPDF },
  { id: "gauss", label: "Gaussian Dist.",      icon: "📊", color: C.gold,    comp: SecGaussian },
  { id: "clt",   label: "Central Limit Thm",  icon: "∑",  color: C.green,   comp: SecCLT },
  { id: "ci",    label: "Confidence Intervals",icon: "📏", color: C.orange,  comp: SecCI },
  { id: "biv",   label: "Bivariate Data",      icon: "🔗", color: "#E879F9", comp: SecBivariate },
  { id: "two",   label: "Two-Sample",          icon: "⚖️", color: C.teal,    comp: SecTwoSample },
  { id: "cov",   label: "Covariance",          icon: "📐", color: "#F472B6", comp: SecCovariance },
  { id: "r2",    label: "Pearson r & r²",      icon: "🎯", color: C.gold,    comp: SecPearsonR2 },
  { id: "spear", label: "Spearman ρ",          icon: "🏅", color: C.purple,  comp: SecSpearman },
  { id: "multi", label: "Normalisation",       icon: "⚙️", color: C.green,   comp: SecMultivariateNorm },
];

export default function App() {
  const [active, setActive] = useState("rv");
  const ActiveComp = SECTIONS.find(s => s.id === active)?.comp;
  const activeS = SECTIONS.find(s => s.id === active);

  return (
    <div style={{ minHeight: "100vh", background: C.bg, color: C.text, fontFamily: "'Segoe UI', system-ui, sans-serif" }}>

      {/* Top header */}
      <div style={{
        background: C.panel, borderBottom: `1px solid ${C.panelBorder}`,
        padding: "14px 24px", display: "flex", alignItems: "center", gap: 16,
        flexWrap: "wrap",
      }}>
        <div>
          <div style={{ fontSize: 11, color: C.muted, letterSpacing: 3, textTransform: "uppercase" }}>Lecture 2 · Visual Guide</div>
          <div style={{ fontSize: 20, fontWeight: 700, color: C.text, fontFamily: "Palatino, serif", letterSpacing: -0.5 }}>
            Statistics: From Random Variables to Multivariate Analysis
          </div>
        </div>
        <div style={{ marginLeft: "auto", fontSize: 12, color: C.muted }}>
          12 Interactive Topics
        </div>
      </div>

      {/* Nav tabs */}
      <div style={{
        background: C.panel, borderBottom: `1px solid ${C.panelBorder}`,
        display: "flex", overflowX: "auto", padding: "0 12px", gap: 2,
      }}>
        {SECTIONS.map(s => (
          <button key={s.id} onClick={() => setActive(s.id)} style={{
            padding: "12px 16px", border: "none", background: "transparent",
            borderBottom: active === s.id ? `2px solid ${s.color}` : "2px solid transparent",
            color: active === s.id ? s.color : C.muted,
            cursor: "pointer", fontSize: 13, fontWeight: active === s.id ? 700 : 400,
            whiteSpace: "nowrap", transition: "all 0.15s",
          }}>
            {s.icon}  {s.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div style={{ maxWidth: 900, margin: "0 auto", padding: "28px 20px 48px" }}>
        {/* Section badge */}
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 24 }}>
          <div style={{
            width: 36, height: 36, borderRadius: 8, background: `${activeS?.color}22`,
            border: `1px solid ${activeS?.color}44`, display: "flex", alignItems: "center",
            justifyContent: "center", fontSize: 18,
          }}>{activeS?.icon}</div>
          <div>
            <div style={{ fontSize: 11, color: C.muted, letterSpacing: 2, textTransform: "uppercase" }}>
              Topic {SECTIONS.findIndex(s => s.id === active) + 1} of {SECTIONS.length}
            </div>
            <div style={{ fontSize: 15, fontWeight: 600, color: activeS?.color }}>{activeS?.label}</div>
          </div>
          {/* Prev/Next */}
          <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
            {SECTIONS.findIndex(s => s.id === active) > 0 && (
              <button onClick={() => setActive(SECTIONS[SECTIONS.findIndex(s => s.id === active) - 1].id)}
                style={{
                  padding: "6px 14px", borderRadius: 6, border: `1px solid ${C.panelBorder}`,
                  background: "transparent", color: C.muted, cursor: "pointer", fontSize: 12,
                }}>← Prev</button>
            )}
            {SECTIONS.findIndex(s => s.id === active) < SECTIONS.length - 1 && (
              <button onClick={() => setActive(SECTIONS[SECTIONS.findIndex(s => s.id === active) + 1].id)}
                style={{
                  padding: "6px 14px", borderRadius: 6, border: `1px solid ${activeS?.color}66`,
                  background: `${activeS?.color}15`, color: activeS?.color, cursor: "pointer", fontSize: 12, fontWeight: 600,
                }}>Next →</button>
            )}
          </div>
        </div>

        {ActiveComp && <ActiveComp />}
      </div>
    </div>
  );
}