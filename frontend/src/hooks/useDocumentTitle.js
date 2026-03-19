// src/hooks/useDocumentTitle.js

import { useEffect } from 'react'

const useDocumentTitle = (title) => {
  useEffect(() => {
    document.title = title ? `${title} | SDD Tickets` : 'SDD Tickets'
  }, [title])
}

export default useDocumentTitle