<template>
  <div class="about-container">

    <!-- Hero -->
    <div class="hero">
      <h1 class="hero-title">Industry Maintenance Platform</h1>
      <p class="hero-subtitle">Industrial Asset, Risk, Management &amp; Technical Monitoring</p>
      <p class="hero-course">Software Project Management &amp; Technical Monitoring Course — Istinye University 2026</p>
    </div>

    <!-- The Problem -->
    <div class="section">
      <div class="section-icon"><i class="pi pi-exclamation-triangle"></i></div>
      <h2>The Problem We Solve</h2>
      <p>
        Industrial plants manage hundreds of PLCs, HMIs, sensors, and network switches.
        In most facilities, this asset data lives in spreadsheets, paper logs, and Visio diagrams
        that are always out of date. Risk assessments happen once a year through an external consultant.
        When a security incident occurs, there is no authoritative record of the asset's last known-good state.
      </p>
      <p>
        Most asset management tools were built for IT environments. They do not understand
        Purdue Model levels, ICS risk scoring, or OT compliance requirements.
        The result is that maintenance supervisors spend hours reconstructing change history from emails
        when an auditor arrives.
      </p>
    </div>

    <!-- The Idea -->
    <div class="section accent">
      <div class="section-icon"><i class="pi pi-lightbulb"></i></div>
      <h2>The Idea</h2>
      <p>
        We adapted an existing open-source industrial CMDB into a complete platform that makes
        asset state <strong>observable</strong>, <strong>continuous</strong>, and <strong>auditable</strong> —
        at zero infrastructure cost.
      </p>
      <p>
        Instead of annual snapshots, the platform tracks every change in real time.
        Instead of spreadsheets, every asset has a structured record with its Purdue level,
        criticality, network interfaces, and a full timeline of modifications.
        Instead of reactive fire-fighting, continuous risk scoring surfaces the highest-risk assets
        every time the dashboard loads.
      </p>
    </div>

    <!-- How It Puts Everything in Order -->
    <div class="section">
      <div class="section-icon"><i class="pi pi-sitemap"></i></div>
      <h2>How It Puts Everything in Order</h2>
      <div class="pillars">
        <div class="pillar">
          <i class="pi pi-server pillar-icon"></i>
          <h3>Asset Management</h3>
          <p>Every device — PLC, HMI, switch, sensor, server — has a structured record covering type, location, interfaces, connections, and documents. Changes are tracked in an immutable audit trail.</p>
        </div>
        <div class="pillar">
          <i class="pi pi-shield pillar-icon"></i>
          <h3>Continuous Risk Scoring</h3>
          <p>Each asset receives an ICS risk score based on its Purdue Model level, business criticality, network exposure, and known vulnerabilities. Scores update automatically on every change.</p>
        </div>
        <div class="pillar">
          <i class="pi pi-chart-line pillar-icon"></i>
          <h3>Management Monitoring</h3>
          <p>A live dashboard tracks project health: sprint velocity, SPI, team workload, milestone status, and cost variance — all from a single API endpoint that refreshes every 60 seconds.</p>
        </div>
        <div class="pillar">
          <i class="pi pi-heart-fill pillar-icon"></i>
          <h3>Technical Monitoring</h3>
          <p>The platform monitors itself. Health endpoints track database connectivity, CPU, memory, and disk. Docker automatically restarts the backend within 90 seconds of a failure — no human action needed.</p>
        </div>
        <div class="pillar">
          <i class="pi pi-users pillar-icon"></i>
          <h3>Role-Based Access</h3>
          <p>Three access levels — Admin, Editor, Viewer — ensure that each team member sees exactly what they need. Multi-tenant architecture keeps organisations isolated from each other.</p>
        </div>
        <div class="pillar">
          <i class="pi pi-check-circle pillar-icon"></i>
          <h3>CI/CD &amp; Testing</h3>
          <p>Every code change runs through GitHub Actions automatically: backend tests against a real PostgreSQL database, frontend Vitest unit tests, and a Vite production build — all at zero cost.</p>
        </div>
      </div>
    </div>

    <!-- Value -->
    <div class="section accent">
      <div class="section-icon"><i class="pi pi-euro"></i></div>
      <h2>Value Created</h2>
      <div class="value-row">
        <div class="value-card">
          <span class="value-number">€0</span>
          <span class="value-label">Infrastructure Cost</span>
          <p>Docker, PostgreSQL, GitHub Actions, Nginx — all open source or free tier.</p>
        </div>
        <div class="value-card">
          <span class="value-number">€110k+</span>
          <span class="value-label">Year 1 Benefit Estimate</span>
          <p>Faster audits, preventive maintenance from continuous risk scores, eliminated consultant fees.</p>
        </div>
        <div class="value-card">
          <span class="value-number">€200k</span>
          <span class="value-label">Commercial Equivalent</span>
          <p>Tools like Claroty and Dragos charge up to €200,000/year for equivalent functionality.</p>
        </div>
      </div>
    </div>

    <!-- Team -->
    <div class="section">
      <div class="section-icon"><i class="pi pi-users"></i></div>
      <h2>The Team</h2>
      <div class="team-grid">
        <div class="team-card" v-for="member in team" :key="member.id">
          <div class="team-avatar">
            <i class="pi pi-user"></i>
          </div>
          <div class="team-info">
            <h3>{{ member.name }}</h3>
            <span class="team-role">{{ member.role }}</span>
            <span class="team-id">ID: {{ member.id }}</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
const team = [
  { name: 'Obada Abdulhakim Kharaz',  id: '2309115277', role: 'Project Manager' },
  { name: 'Mohanad Aref Ali Sultan',  id: '2309115898', role: 'Backend Developer' },
  { name: 'Zekeriya Dulli',           id: '2309115377', role: 'Frontend Developer' },
  { name: 'Praise-God Tobby',         id: '2309116418', role: 'QA / Test Engineer' },
  { name: 'Fares Stouhi',             id: '2309115179', role: 'UX / UI Designer' },
  { name: 'Hamdi Alnaqeeb',           id: '2309116178', role: 'DevOps / Operations' },
  { name: 'Abdulaziz Alyahya',        id: '2309116441', role: 'Risk Manager' },
]
</script>

<style scoped>
.about-container {
  max-width: 1100px;
  margin: 0 auto;
  padding-bottom: 3rem;
}

/* Hero */
.hero {
  text-align: center;
  padding: 3rem 2rem 2rem;
  margin-bottom: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: #fff;
}

.hero-title {
  font-size: 2.4rem;
  font-weight: 700;
  margin: 0 0 0.5rem;
}

.hero-subtitle {
  font-size: 1.1rem;
  margin: 0 0 0.5rem;
  opacity: 0.9;
}

.hero-course {
  font-size: 0.9rem;
  opacity: 0.75;
  margin: 0;
}

/* Sections */
.section {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 2rem 2.5rem;
  margin-bottom: 1.5rem;
}

.section.accent {
  background: #f5f3ff;
  border-color: #c4b5fd;
}

.section-icon {
  font-size: 1.6rem;
  color: #6366f1;
  margin-bottom: 0.75rem;
}

.section h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e1b4b;
  margin: 0 0 1rem;
}

.section p {
  color: #4b5563;
  line-height: 1.75;
  margin: 0 0 0.75rem;
}

/* Pillars */
.pillars {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-top: 1rem;
}

.pillar {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
}

.pillar-icon {
  font-size: 1.6rem;
  color: #6366f1;
  margin-bottom: 0.75rem;
  display: block;
}

.pillar h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1e1b4b;
  margin: 0 0 0.5rem;
}

.pillar p {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}

/* Value cards */
.value-row {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.25rem;
  margin-top: 1rem;
}

.value-card {
  background: #fff;
  border: 1px solid #c4b5fd;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
}

.value-number {
  display: block;
  font-size: 2rem;
  font-weight: 800;
  color: #6366f1;
  margin-bottom: 0.25rem;
}

.value-label {
  display: block;
  font-weight: 600;
  color: #1e1b4b;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.value-card p {
  font-size: 0.8rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

/* Team */
.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.team-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem 1.25rem;
}

.team-avatar {
  width: 46px;
  height: 46px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.team-info h3 {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1e1b4b;
  margin: 0 0 0.2rem;
}

.team-role {
  display: block;
  font-size: 0.8rem;
  color: #6366f1;
  font-weight: 500;
}

.team-id {
  display: block;
  font-size: 0.75rem;
  color: #9ca3af;
  margin-top: 0.1rem;
}
</style>
