import { Backdrop, SpeedDial, SpeedDialAction } from '@mui/material'
import React from 'react';
import SignalCellularAltIcon from '@mui/icons-material/SignalCellularAlt';
import SignalCellularAlt2BarIcon from '@mui/icons-material/SignalCellularAlt2Bar';
import SignalCellularAlt1BarIcon from '@mui/icons-material/SignalCellularAlt1Bar';
import { useDataContext } from './DataProvider';
import { useThemeContext } from './ThemeProvider';
import NightsStayIcon from '@mui/icons-material/NightsStay';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import CottageIcon from '@mui/icons-material/Cottage';
import PsychologyIcon from '@mui/icons-material/Psychology';
import deleteChosenModel from '../../routes/removeChosenModel';

function Header() {
  const {isDarkMode,toggleTheme} = useThemeContext();
  const {modelName,setModelName} = useDataContext();
  const [open, setOpen] = React.useState(false);
  const latency = useDataContext().latency;
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  
  const getLatencyIcon = () => {
    if(latency == null || latency > 700){
      return <SignalCellularAlt1BarIcon />
    }else if(latency > 400){
      return <SignalCellularAlt2BarIcon />
    }else{
      return <SignalCellularAltIcon />
    }
  }

  const removeCurrentModel = () => {
    deleteChosenModel().then(res=>{
      if(res){
        setModelName(null)
      }
    })
  }

  const actions = [
    { icon: isDarkMode?<NightsStayIcon />:<WbSunnyIcon /> , name: 'Tema',method:toggleTheme },
    { icon: getLatencyIcon() , name: "latenza: "+ (latency!= null ?latency:0) +"ms",method:()=>{} },
    { icon: <PsychologyIcon /> , name: modelName,method:removeCurrentModel },
  ];


  return (
    <>
    <Backdrop open={open} />
    <SpeedDial
      ariaLabel="SpeedDial tooltip example"
      sx={{ position: 'absolute', bottom: 16, right: 16 }}
      icon={<CottageIcon />}
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
  )
}

export default Header