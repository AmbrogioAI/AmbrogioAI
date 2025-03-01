import { Backdrop, SpeedDial, SpeedDialAction } from "@mui/material";
import React from "react";
import SignalCellularAltIcon from "@mui/icons-material/SignalCellularAlt";
import SignalCellularAlt2BarIcon from "@mui/icons-material/SignalCellularAlt2Bar";
import SignalCellularAlt1BarIcon from "@mui/icons-material/SignalCellularAlt1Bar";
import { useDataContext } from "./DataProvider";
import { useThemeContext } from "./ThemeProvider";
import NightsStayIcon from "@mui/icons-material/NightsStay";
import WbSunnyIcon from "@mui/icons-material/WbSunny";
import PsychologyIcon from "@mui/icons-material/Psychology";
import deleteChosenModel from "../../routes/removeChosenModel";
import { Language, t } from "../../translations/t";
import UnitedKingdomFlag from "../../icons/UnitedKingdomFlag";
import ItalianFlag from "../../icons/ItalianFlag";
import DashboardIcon from '@mui/icons-material/Dashboard';

function Header() {
  const { isDarkMode, toggleTheme } = useThemeContext();
  const { modelName, setModelName, language, setLanguage } = useDataContext();
  const [open, setOpen] = React.useState(false);
  const latency = useDataContext().latency;
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const getLatencyIcon = () => {
    if (latency == null || latency > 700) {
      return <SignalCellularAlt1BarIcon />;
    } else if (latency > 400) {
      return <SignalCellularAlt2BarIcon />;
    } else {
      return <SignalCellularAltIcon />;
    }
  };

  const removeCurrentModel = () => {
    deleteChosenModel().then((res) => {
      if (res) {
        setModelName(null);
      }
    });
  };

  const actions = [
    {
      icon: getLatencyIcon(),
      name: t("latency",language) + (latency != null ? latency : 0) + "ms",
      method: () => {},
    },
    {
      icon: language == Language.EN ? <UnitedKingdomFlag width={30} height={30} /> : <ItalianFlag width={30} height={30} />,
      name: t("Language", language),
      method:()=> setLanguage(language == Language.EN ? Language.IT : Language.EN),
    },
    {
      icon: isDarkMode ? <NightsStayIcon /> : <WbSunnyIcon />,
      name: t("Theme", language),
      method: toggleTheme,
    },
    { icon: <PsychologyIcon />, name: modelName??t("noModel",language), method: removeCurrentModel },
  ];

  return (
    <>
      <Backdrop open={open} />
      <SpeedDial
        ariaLabel="SpeedDial tooltip example"
        sx={{ position: "fixed", bottom: 16, right: 16 }}
        icon={<DashboardIcon />}
        onClose={handleClose}
        onOpen={handleOpen}
        open={open}
      >
        {actions.map((action) => (
          <SpeedDialAction
            key={action.name}
            icon={action.icon}
            tooltipTitle={action.name}
            tooltipOpen
            onClick={action.method}
          />
        ))}
      </SpeedDial>
    </>
  );
}

export default Header;
