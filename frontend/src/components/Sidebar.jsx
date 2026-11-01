
import {
  LayoutDashboard,
  Wind,
  ChartNoAxesCombined,
  Settings,
  Zap
} from "lucide-react";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">
          <Wind size={22} />
        </div>
        <div>
          <h2>WindSight</h2>
          <span>ENERGY INTELLIGENCE</span>
        </div>
      </div>

      <div className="sidebar-section">
        <p className="sidebar-label">WORKSPACE</p>

        <div className="nav-item active">
          <LayoutDashboard size={18} />
          <span>Overview</span>
        </div>

        <div className="nav-item">
          <ChartNoAxesCombined size={18} />
          <span>Forecast Analysis</span>
        </div>

        <div className="nav-item">
          <Wind size={18} />
          <span>Wind Generation</span>
        </div>
      </div>

      <div className="sidebar-bottom">
        <div className="nav-item">
          <Settings size={18} />
          <span>Settings</span>
        </div>

        <div className="sidebar-status">
          <Zap size={16} />
          <span>January 2026 Dataset</span>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
