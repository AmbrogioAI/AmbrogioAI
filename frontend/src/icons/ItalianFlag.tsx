import React from 'react'

function ItalianFlag(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      shapeRendering="geometricPrecision"
      textRendering="geometricPrecision"
      imageRendering="optimizeQuality"
      fillRule="evenodd"
      viewBox="0 0 55.2 38.4"
      {...props}
    >
      <g fillRule="nonzero">
        <path fill="#009246" d="M0 0h18.4v38.4H0z" />
        <path fill="#fff" d="M18.4 0h18.4v38.4H18.4z" />
        <path fill="#CE2B37" d="M36.8 0h18.4v38.4H36.8z" />
      </g>
    </svg>
)
}

export default ItalianFlag