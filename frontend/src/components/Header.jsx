
import { CalendarDays, ChevronDown } from "lucide-react";

function Header() {
  return (
    <header className="header">
      <div>
        <h1>Wind Generation Overview</h1>
        <p>National wind forecast performance and accuracy</p>
      </div>

      <div className="header-date">
        <CalendarDays size={18} />
        <span>January 2026</span>
        <ChevronDown size={16} />
      </div>
    </header>
  );
}

export default Header;
