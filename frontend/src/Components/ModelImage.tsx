import { PossibleModels } from '../routes/chooseModel'
import resNet from "../images/resNet.png"
import simple from "../images/simple.png"

interface ModelImageProps {
    model: PossibleModels,
    size: number
    showShadow?: boolean
}

function ModelImage({model, size, showShadow}: ModelImageProps) {
    const img = model === PossibleModels.resNet50 ? resNet:simple
    showShadow = showShadow ?? false
    
  return (
        <img
        style={{ width: size, height: size, objectFit: "contain",filter: showShadow ? "drop-shadow(#5EB0E8 -60px 30px 190px)":"none" }}
        src={`${img}?w=${size}&h=${size}&fit=crop&auto=format`}
        alt={"model"+model}
        loading="lazy"
      />
    )
}

export default ModelImage