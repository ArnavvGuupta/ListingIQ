
import { useEffect, useMemo, useState } from "react";
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
    ResponsiveContainer, PieChart, Pie, Cell, Legend
} from "recharts";
import {
    Building2, MapPin, Tags, Database, RefreshCw, Search,
    LayoutDashboard, BriefcaseBusiness, ChartNoAxesCombined,
    ChevronRight, Activity, CheckCircle2, AlertCircle
} from "lucide-react";

import {
    getSummary, getCities, getCategories, getSources, getListings
} from "./services/api";

import "./App.css";

const COLORS = [
    "#6366F1", "#06B6D4", "#10B981", "#F59E0B",
    "#F43F5E", "#8B5CF6", "#0EA5E9", "#84CC16", "#94A3B8"
];

function StatCard({ title, value, icon: Icon, color, description }) {
    return (
        <article className="stat-card">
            <div className="stat-card-top">
                <div className={`stat-icon ${color}`}>
                    <Icon size={21} strokeWidth={2} />
                </div>
                <span className="stat-caption">Database metric</span>
            </div>
            <p className="stat-title">{title}</p>
            <div className="stat-value-row">
                <h2>{Number(value ?? 0).toLocaleString()}</h2>
                <span className="stat-check"><CheckCircle2 size={15} /></span>
            </div>
            <p className="stat-description">{description}</p>
        </article>
    );
}

function ChartCard({ title, subtitle, children, className = "" }) {
    return (
        <section className={`chart-card ${className}`}>
            <div className="chart-heading">
                <div>
                    <h3>{title}</h3>
                    <p>{subtitle}</p>
                </div>
                <span className="chart-menu" aria-hidden="true">•••</span>
            </div>
            {children}
        </section>
    );
}

function EmptyChart() {
    return <div className="chart-empty">No chart data available yet.</div>;
}

export default function App() {
    const [summary, setSummary] = useState(null);
    const [cities, setCities] = useState([]);
    const [categories, setCategories] = useState([]);
    const [sources, setSources] = useState([]);
    const [listings, setListings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState("");
    const [search, setSearch] = useState("");
    const [cityFilter, setCityFilter] = useState("All cities");
    const [categoryFilter, setCategoryFilter] = useState("All categories");

    async function loadDashboard(isRefresh = false) {
        if (isRefresh) setRefreshing(true);
        else setLoading(true);
        setError("");

        try {
            const [s, cityData, categoryData, sourceData, listingData] =
                await Promise.all([
                    getSummary(),
                    getCities(),
                    getCategories(),
                    getSources(),
                    getListings(),
                ]);

            setSummary(s);
            setCities(cityData);
            setCategories(categoryData);
            setSources(sourceData);
            setListings(listingData);
        } catch (err) {
            setError(err.message || "Unable to load dashboard data.");
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    }

    useEffect(() => {
        loadDashboard();
    }, []);

    const topCities = useMemo(
        () => [...cities].sort((a, b) => b.count - a.count).slice(0, 10),
        [cities]
    );

    const categoryChartData = useMemo(() => {
        const sorted = [...categories].sort((a, b) => b.count - a.count);
        const top = sorted.slice(0, 8);
        const other = sorted.slice(8).reduce((sum, item) => sum + item.count, 0);
        return other > 0 ? [...top, { name: "Other", count: other }] : top;
    }, [categories]);

    const cityOptions = useMemo(
        () => [...new Set(listings.map((item) => item.city).filter(Boolean))].sort(),
        [listings]
    );

    const categoryOptions = useMemo(
        () => [...new Set(listings.map((item) => item.category).filter(Boolean))].sort(),
        [listings]
    );

    const filteredListings = useMemo(() => {
        const term = search.trim().toLowerCase();

        return listings.filter((item) => {
            const matchesSearch =
                !term ||
                [item.business_name, item.city, item.category, item.phone, item.address]
                    .some((value) => String(value || "").toLowerCase().includes(term));

            const matchesCity =
                cityFilter === "All cities" || item.city === cityFilter;

            const matchesCategory =
                categoryFilter === "All categories" ||
                item.category === categoryFilter;

            return matchesSearch && matchesCity && matchesCategory;
        });
    }, [listings, search, cityFilter, categoryFilter]);

    if (loading) {
        return (
            <main className="loading-screen">
                <div className="loading-mark"><Building2 size={30} /></div>
                <div className="loading-spinner" />
                <h2>Preparing your dashboard</h2>
                <p>Connecting to your business intelligence database…</p>
            </main>
        );
    }

    if (error) {
        return (
            <main className="error-screen">
                <div className="error-icon"><AlertCircle size={28} /></div>
                <h2>Unable to load dashboard</h2>
                <p>{error}</p>
                <button className="primary-button" onClick={() => loadDashboard()}>
                    <RefreshCw size={16} /> Try again
                </button>
            </main>
        );
    }

    return (
        <div className="app-shell">
            <aside className="sidebar">
                <div className="brand">
                    <div className="brand-mark"><Building2 size={23} /></div>
                    <div className="brand-copy">
                        <strong>Listing<span>IQ</span></strong>
                        <small>BUSINESS INTELLIGENCE</small>
                    </div>
                </div>

                <div className="sidebar-label">WORKSPACE</div>
                <nav className="sidebar-nav">
                    <a className="nav-item active" href="#overview">
                        <LayoutDashboard size={18} />
                        <span>Overview</span>
                        <ChevronRight className="nav-chevron" size={15} />
                    </a>
                    <a className="nav-item" href="#listings">
                        <BriefcaseBusiness size={18} />
                        <span>Business listings</span>
                    </a>
                    <a className="nav-item" href="#analytics">
                        <ChartNoAxesCombined size={18} />
                        <span>Analytics</span>
                    </a>
                </nav>

                <div className="sidebar-bottom">
                    <div className="database-status">
                        <span className="status-dot" />
                        <div>
                            <strong>System operational</strong>
                            <small>Dashboard services</small>
                        </div>
                    </div>
                    <div className="sidebar-profile">
                        <div className="profile-avatar">BL</div>
                        <div className="profile-copy">
                            <strong>Listings Admin</strong>
                            <small>Workspace overview</small>
                        </div>
                    </div>
                </div>
            </aside>

            <main className="main-content" id="overview">
                <header className="topbar">
                    <div className="breadcrumb">
                        Workspace <ChevronRight size={14} /> <strong>Overview</strong>
                    </div>
                    <div className="topbar-right">
                        <span className="live-badge"><span className="status-dot" /> Live data</span>
                        <button
                            className="refresh-button"
                            onClick={() => loadDashboard(true)}
                            disabled={refreshing}
                        >
                            <RefreshCw size={16} className={refreshing ? "spin" : ""} />
                            {refreshing ? "Refreshing…" : "Refresh data"}
                        </button>
                    </div>
                </header>

                <section className="page-intro">
                    <div>
                        <p className="eyebrow"><Activity size={14} /> BUSINESS ANALYTICS</p>
                        <h1>Business overview</h1>
                        <p className="page-subtitle">
                            Your business data, organized into one clear picture.
                        </p>
                    </div>
                    <div className="date-chip">
                        <Database size={16} />
                        <span>MySQL database</span>
                    </div>
                </section>

                <section className="stats-grid">
                    <StatCard
                        title="Total listings"
                        value={summary?.total_listings}
                        icon={Building2}
                        color="indigo"
                        description="Records in dashboard sample"
                    />
                    <StatCard
                        title="Cities covered"
                        value={summary?.cities}
                        icon={MapPin}
                        color="cyan"
                        description="Distinct locations represented"
                    />
                    <StatCard
                        title="Categories"
                        value={summary?.categories}
                        icon={Tags}
                        color="green"
                        description="Business types identified"
                    />
                    <StatCard
                        title="Data sources"
                        value={summary?.sources}
                        icon={Database}
                        color="amber"
                        description="Sources represented in records"
                    />
                </section>

                <section className="analytics-section" id="analytics">
                    <div className="section-heading">
                        <div>
                            <h2>Analytics & insights</h2>
                            <p>Explore how your listings are distributed.</p>
                        </div>
                        <span className="section-tag">INTERACTIVE REPORTS</span>
                    </div>

                    <div className="charts-grid">
                        <ChartCard
                            title="Top 10 cities"
                            subtitle="Listings by location"
                            className="city-chart-card"
                        >
                            {topCities.length ? (
                                <ResponsiveContainer width="100%" height={310}>
                                    <BarChart data={topCities} margin={{ top: 12, right: 8, left: -18, bottom: 55 }}>
                                        <CartesianGrid stroke="#EDF0F5" strokeDasharray="4 4" vertical={false} />

                                        <XAxis
                                            dataKey="name"
                                            interval={0}
                                            angle={-30}
                                            textAnchor="end"
                                            height={75}
                                            tick={{ fontSize: 10, fill: "#7C8498" }}
                                            tickFormatter={(name) =>
                                                name.length > 12 ? `${name.slice(0, 12)}…` : name
                                            }
                                            axisLine={false}
                                            tickLine={false}
                                        />

                                        <YAxis
                                            allowDecimals={false}
                                            tick={{ fontSize: 11, fill: "#7C8498" }}
                                            axisLine={false}
                                            tickLine={false}
                                        />

                                        <Tooltip
                                            cursor={{ fill: "#F3F4FF" }}
                                            allowEscapeViewBox={{ x: false, y: false }}
                                            wrapperStyle={{ zIndex: 10, maxWidth: "170px" }}
                                            contentStyle={{
                                                borderRadius: 12,
                                                border: "1px solid #E8EAF2",
                                                boxShadow: "0 8px 24px #18213B12",
                                                fontSize: 12
                                            }}
                                        />

                                        <Bar dataKey="count" name="Listings" fill="#6366F1" radius={[6, 6, 0, 0]} maxBarSize={42} />
                                    </BarChart>
                                </ResponsiveContainer>
                            ) : <EmptyChart />}
                        </ChartCard>

                        <ChartCard
                            title="Category breakdown"
                            subtitle="Share of listings by business type"
                        >
                            {categoryChartData.length ? (
                                <ResponsiveContainer width="100%" height={310}>
                                    <PieChart>
                                        <Pie
                                            data={categoryChartData}
                                            dataKey="count"
                                            nameKey="name"
                                            cx="50%"
                                            cy="43%"
                                            innerRadius={62}
                                            outerRadius={96}
                                            paddingAngle={3}
                                            stroke="none"
                                        >
                                            {categoryChartData.map((item, index) => (
                                                <Cell key={item.name} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip
                                            contentStyle={{ borderRadius: 12, border: "1px solid #E8EAF2" }}
                                        />
                                        <Legend
                                            verticalAlign="bottom"
                                            align="center"
                                            height={62}
                                            wrapperStyle={{ fontSize: 11, color: "#626B80" }}
                                        />
                                    </PieChart>
                                </ResponsiveContainer>
                            ) : <EmptyChart />}
                        </ChartCard>

                        <ChartCard
                            title="Source distribution"
                            subtitle="Where your business data comes from"
                        >
                            {sources.length ? (
                                <ResponsiveContainer width="100%" height={310}>
                                    <PieChart>
                                        <Pie
                                            data={sources}
                                            dataKey="count"
                                            nameKey="name"
                                            cx="50%"
                                            cy="43%"
                                            innerRadius={62}
                                            outerRadius={96}
                                            paddingAngle={3}
                                            stroke="none"
                                        >
                                            {sources.map((item, index) => (
                                                <Cell key={item.name} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip
                                            contentStyle={{ borderRadius: 12, border: "1px solid #E8EAF2" }}
                                        />
                                        <Legend
                                            verticalAlign="bottom"
                                            align="center"
                                            height={62}
                                            wrapperStyle={{ fontSize: 11, color: "#626B80" }}
                                        />
                                    </PieChart>
                                </ResponsiveContainer>
                            ) : <EmptyChart />}
                        </ChartCard>
                    </div>
                </section>

                <section className="table-card" id="listings">
                    <div className="table-heading">
                        <div>
                            <p className="eyebrow">YOUR DIRECTORY</p>
                            <h2>Business listings</h2>
                            <p>Search and filter records in your current dashboard sample.</p>
                        </div>
                        <span className="record-count">
                            {filteredListings.length} <span>of {listings.length} records</span>
                        </span>
                    </div>

                    <div className="table-toolbar">
                        <div className="search-box">
                            <Search size={17} />
                            <input
                                type="search"
                                placeholder="Search business, city, phone…"
                                value={search}
                                onChange={(event) => setSearch(event.target.value)}
                            />
                        </div>
                        <select
                            aria-label="Filter by city"
                            value={cityFilter}
                            onChange={(event) => setCityFilter(event.target.value)}
                        >
                            <option>All cities</option>
                            {cityOptions.map((city) => <option key={city}>{city}</option>)}
                        </select>
                        <select
                            aria-label="Filter by category"
                            value={categoryFilter}
                            onChange={(event) => setCategoryFilter(event.target.value)}
                        >
                            <option>All categories</option>
                            {categoryOptions.map((category) => <option key={category}>{category}</option>)}
                        </select>
                    </div>

                    <div className="table-scroll">
                        <table>
                            <thead>
                                <tr>
                                    <th>BUSINESS</th>
                                    <th>CATEGORY</th>
                                    <th>CITY</th>
                                    <th>PHONE</th>
                                    <th>SOURCE</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredListings.map((item) => (
                                    <tr key={item.id}>
                                        <td>
                                            <div className="business-cell">
                                                <div className="business-avatar">
                                                    {(item.business_name || "B").trim().charAt(0).toUpperCase()}
                                                </div>
                                                <div className="business-info">
                                                    <strong>{item.business_name}</strong>
                                                    <small>{item.address || "Address not provided"}</small>
                                                </div>
                                            </div>
                                        </td>
                                        <td><span className="category-tag">{item.category || "Uncategorized"}</span></td>
                                        <td><span className="city-cell"><MapPin size={13} /> {item.city || "—"}</span></td>
                                        <td className="phone-cell">{item.phone || "—"}</td>
                                        <td><span className="source-tag">{item.source}</span></td>
                                    </tr>
                                ))}
                                {filteredListings.length === 0 && (
                                    <tr>
                                        <td colSpan="5" className="empty-cell">
                                            No listings match your search or filters.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                    <div className="table-footer">
                        <span>Showing filtered results from the records returned by your API.</span>
                        <button
                            className="clear-filters"
                            onClick={() => {
                                setSearch("");
                                setCityFilter("All cities");
                                setCategoryFilter("All categories");
                            }}
                        >
                            Clear filters
                        </button>
                    </div>
                </section>

                <footer className="app-footer">
                    <span>ListingIQ <span className="footer-dot">•</span> Business intelligence dashboard</span>
                    <span>Built with React, FastAPI & MySQL</span>
                </footer>
            </main>
        </div>
    );
}
