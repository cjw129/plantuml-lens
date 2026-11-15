# Third party notices

PlantUML Lens is MIT licensed (see [LICENSE](LICENSE)). It started as a fork of [plantuml/plantuml-for-github](https://github.com/plantuml/plantuml-for-github) (MIT). It bundles the components below. Licenses are the ones declared by the upstream projects, check the upstream repositories for the authoritative text.

## PlantUML engine (`extension/vendor/plantuml.js`)

[PlantUML](https://github.com/plantuml/plantuml) compiled to JavaScript with [TeaVM](https://github.com/konsoletyper/teavm) (Apache-2.0, the TeaVM runtime is part of the compiled output). PlantUML is offered by its authors under several licenses (GPL, LGPL, Apache, EPL and MIT, "you can choose the one that suits you best"). The engine file is a copy of the build that the PlantUML project publishes at https://plantuml.github.io/plantuml/js-plantuml/ and carries no license header of its own. It is distributed here under the MIT option, which matches the MIT license of this repository. The graph layout is Smetana, PlantUML's Java port of Graphviz, compiled into the same file.

## Standard library bundles (`extension/*.min.js`)

Byte for byte copies of the files published by the PlantUML project, refreshed with `fetch_stdlib.py`. They are sprite and macro collections, mostly made from other projects' icons. The upstream repositories, as listed on https://plantuml.com/stdlib:

| Bundle | Upstream |
| :- | :- |
| `archimate` | https://github.com/ebbypeter/Archimate-PlantUML |
| `awslib`, `awslib10`, `awslib14`, `awslib20` | https://github.com/awslabs/aws-icons-for-plantuml |
| `azure` | https://github.com/RicardoNiepel/Azure-PlantUML |
| `c4`, `classy-c4` | https://github.com/plantuml-stdlib/C4-PlantUML |
| `cloudinsight` | https://github.com/rabelenda/cicon-plantuml-sprites |
| `cloudogu` | https://github.com/cloudogu/plantuml-cloudogu-sprites |
| `edgy` | https://github.com/boessu/plantuml-stdlib/tree/master/edgy |
| `elastic` | https://github.com/Crashedmind/PlantUML-Elastic-icons |
| `material`, `material2`, `material2.1.19` | https://github.com/Templarian/MaterialDesign |
| `kubernetes`, `k8s` | https://github.com/michiel/plantuml-kubernetes-sprites |
| `logos` | https://github.com/plantuml-stdlib/gilbarbara-plantuml-sprites |
| `office` | https://github.com/Roemer/plantuml-office |
| `osa`, `osa2` | https://github.com/Crashedmind/PlantUML-opensecurityarchitecture-icons, https://github.com/Crashedmind/PlantUML-opensecurityarchitecture2-icons |
| `tupadr3` | https://github.com/tupadr3/plantuml-icon-font-sprites (includes Font Awesome, Devicons and other icon sets) |
| `adaml`, `bootstrap`, `bootstrap1.13.1`, `classy`, `domainstory`, `eip`, `gcp`, `ibm` | part of the PlantUML stdlib, the upstream is not listed on the stdlib page |

The license of each upstream project, and the terms of the vendors whose icons are redrawn in them (AWS, Microsoft Azure and Office, Google Cloud, IBM, Kubernetes, Elastic and others), were **not** reviewed here: several icon sets come with trademark or brand usage terms in addition to the license of the sprite files. Review the upstream repositories before you redistribute a build of this extension, and drop the bundles you do not need from `STDLIB_BUNDLES` in `fetch_stdlib.py` and `build_zip.py`, and from `extension/manifest.json`.

## Support scripts

`extension/emoji.js`, `extension/themes.js` and `extension/openiconic.js` are copies of the files that the PlantUML project publishes next to the engine (emoji sprites, the `!theme` definitions and the [Open Iconic](https://github.com/iconic/open-iconic) sprites, MIT / SIL OFL 1.1).

## Names

"PlantUML" is the name of the PlantUML project. PlantUML Lens is an independent extension and is not affiliated with or endorsed by it. The icons of this extension are original.