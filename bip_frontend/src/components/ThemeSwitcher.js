import React from "react";
import Toggle from "react-toggle";
import { useColorScheme } from "../hooks/useColorScheme";
const ThemeSwitcher = () => {
    const { isDark, setIsDark } = useColorScheme();

    return (
        <Toggle className="theme-switcher"
            checked={isDark}
            onChange={({ target }) => setIsDark(target.checked)}
            icons={false}
            aria-label="Theme toggler"
        />
    )
}

export default ThemeSwitcher;