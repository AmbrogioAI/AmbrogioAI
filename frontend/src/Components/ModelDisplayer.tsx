import { t } from '../translations/t'
import { useDataContext } from './Layout/DataProvider'

function ModelDisplayer() {
  const {language} = useDataContext()
  return (
    <div>{t("ModelDisplayer",language)}</div>
  )
}

export default ModelDisplayer