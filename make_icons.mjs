// Renders extension/icons/icon.svg into extension/icons/icon<size>.png.
//
//   mkdir /tmp/icons && cd /tmp/icons && npm i @resvg/resvg-js
//   node <repo>/make_icons.mjs <repo>      (run from the directory above)
import fs from 'node:fs'
import path from 'node:path'
import {createRequire} from 'node:module'

var {Resvg} = createRequire(path.join(process.cwd(), '/'))('@resvg/resvg-js')
var root = path.resolve(process.argv[2] || '.')
var dir = path.join(root, 'extension', 'icons')
var svg = fs.readFileSync(path.join(dir, 'icon.svg'), 'utf8')

for (var size of [16, 48, 128]) {
  var png = new Resvg(svg, {fitTo: {mode: 'width', value: size}}).render().asPng()
  fs.writeFileSync(path.join(dir, `icon${size}.png`), png)
}
console.log('icons written')