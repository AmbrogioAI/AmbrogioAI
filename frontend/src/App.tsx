import "./App.css";
import Helmet from "./Components/Layout/Helmet";
import ModelPicker from "./Components/ModelPicker";
import { useDataContext } from "./Components/Layout/DataProvider";
import ModelDisplayer from "./Components/ModelDisplayer";

function App() {

  return <Helmet title="App">{useDataContext().modelName === null ? <ModelPicker />:<ModelDisplayer />}</Helmet>;
}

export default App;
