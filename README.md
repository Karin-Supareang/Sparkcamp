# LectureCheck — Professor Dashboard (MVP Prototype)

Welcome to the **LectureCheck** early prototype dashboard! This is the results screen designed for professors to evaluate class-wide comprehension in real time after uploading lecture slides.

---

## 🚀 Getting Started

To run the dashboard prototype locally, execute the following commands in your terminal:

```bash
# Navigate to the project folder
cd project

# Install Vite and React dependencies
npm install

# Spin up the local development server
npm run dev
```

The app will start running at `http://localhost:5173/` by default.

---

## 🎨 Visual Design & UX Highlights

This prototype was crafted using opinionated design standards prioritizing visual aesthetics, high glanceability, and accessibility (WCAG AA compliant). 

Key design elements implemented in this build:

### 1. WCAG AA Compliant Golden Theme
Yellow and gold can be notoriously difficult to design with for web accessibility. We avoided loud neon highlights by establishing a refined golden-amber color system:
- **Calm, High-contrast base:** Uses warm neutral backgrounds (`hsl(45, 20%, 98%)`) paired with deep charcoal headings (`hsl(40, 25%, 12%)`).
- **Semantic Feedback Range:** Question scores render in three distinct bands:
  - 🟢 **Teal/Green** for high comprehension ($\ge 80\%$)
  - 🟡 **Amber/Gold** for warnings ($50\% - 79\%$), darkened to a compliant `hsl(38, 85%, 38%)` to satisfy WCAG AA contrast against white card panels.
  - 🔴 **Rose/Red** for critical concepts ($< 50\%$).
- **Legible Metadata:** Light helper texts are set to a minimum `4.6:1` contrast ratio to ensure readability for low-vision users.

### 2. Extruding Collapse Sidebar (Desktop)
- The sidebar library panel collapses from `260px` down to a compact `72px` layout on desktop.
- Toggle control is styled as a vertical floating tab that **extrudes outside** the right-hand border of the sidebar.
- Features a dynamic **Chevron toggle** that slides and rotates 180° smoothly on layout changes.
- Automatically disabled on mobile viewports to preserve touch targets.

### 3. Screen-Sharing Safe "Theater Mode"
- Projecting student results in front of a lecture hall can bias student responses and cause anxiety.
- **Project Join Screen:** A dedicated modal can be launched from the QR card. It overlays the entire screen in a dark, high-contrast theme, displaying *only* a large QR code, a copyable share URL (`check.lec/4921`), and a connected student counter, keeping dashboard statistics completely private.

### 4. Zero Layout-Shift Skeletons
- The skeleton loading loaders are unified across both the **idle state** (no lecture loaded) and the **uploading state** (during analysis).
- The shimmering placeholder elements mirror the exact grid columns (`2.2fr 1fr`) of the populated dashboard, eliminating layout reflow when slides are processed.
- Animates a soft, bright glow sweep over a secondary base rather than solid dark sweeps to maintain a premium feel.

### 5. Interactive Question Accordion & Distractor Heatmap
- Question performance results are expandable accordions using a CSS Grid height transition (`grid-template-rows: 0fr -> 1fr`) for smooth slide-down motions without document jumps.
- Fully focusable and keyboard-navigable (`tabIndex={0}`, Enter/Space key listeners).
- **Critical Distractors:** Incorrect answers that drew $\ge 25\%$ of the class are highlighted in warning red with a *"Common Error"* badge, pointing out exactly what concept needs clarification in under 5 seconds of scanning.

---

## 📁 Codebase Directory Map

- `src/App.jsx` — Core React component handling file upload states, interactive accordion toggles, join modals, and SVG icon components.
- `src/index.css` — Stylesheet housing color systems, typography scale, 8px grid variables, layout grids, mobile responsive overrides, and GPU compositor shimmers.
