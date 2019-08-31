//Dont change it
requirejs(['ext_editor_io', 'jquery_190', 'raphael_210'],
    function (extIO, $) {
        function hexagonalIslandsCanvas(dom, data) {

            if (! data || ! data.ext) {
                return
            }

            const result = data.ext.result
            const output = data.out
            const input = data.in
            const explanation = data.ext.explanation

            /*----------------------------------------------*
             *
             * attr
             *
             *----------------------------------------------*/
            const attr = {
                edge: {
                    'stroke-width': 0.5,
                    'stroke': '#8fc7ed',
                },
                hexagon: {
                    island: {
                        'fill': '#8fc7ed',
                        'stroke': '#4094c7',
                    },
                    inland: {
                        'fill': '#4094c7',
                        'stroke': '#4094c7',
                    },
                }
            }

            /*----------------------------------------------*
             *
             * paper
             *
             *----------------------------------------------*/
            const [ROW, COL] = [9, 12]
            const R = 19
            const H = Math.sqrt(Math.pow(R, 2)-Math.pow(R/2, 2))
            const os = 10

            const paper_w = R*1.5*COL+R/2+os*2
            const paper_h = H*2*ROW+H+os*2
            const paper = Raphael(dom, paper_w, paper_h, 0, 0);

            /*----------------------------------------------*
             *
             * draw
             *
             *----------------------------------------------*/
            let hexagon_dict = {}

            draw_hex_grid(ROW, COL)

            for (hex of input) {
                hexagon_dict[hex].attr(attr.hexagon.island)
            }
            for (hex of explanation) {
                hexagon_dict[hex].attr(attr.hexagon.inland)
            }

            /*----------------------------------------------*
             *
             * draw hex grid
             *
             *----------------------------------------------*/
            function draw_hex_grid(row, col, borders) {
                for (let r = 0; r < row; r += 1) {
                    for (let c = 0; c < col; c += 1) {
                        const [cx, cy]
                            = [c*R*1.5+R+os, r*H*2+(H*(c%2))+H+os]
                        const fig = String.fromCodePoint(c+65)+(r+1)
                        hexagon_dict[fig] = draw_hex(cx, cy)
                        paper.text(cx, cy, fig).attr({'font-size': '9px', 'fill': 'black'})
                    }
                }
            }

            /*----------------------------------------------*
             *
             * draw hex
             *
             *----------------------------------------------*/
            function draw_hex(cx, cy) {
                let deg = -120
                let hexagon_path = ['M']
                for (let i = 0; i < 6; i += 1) {
                    const x1 = Math.cos(Math.PI*2*((deg+i*60)/360))*R
                    const y1 = Math.sin(Math.PI*2*((deg+i*60)/360))*R
                    const x2 = Math.cos(Math.PI*2*((deg+(i+1)*60)/360))*R
                    const y2 = Math.sin(Math.PI*2*((deg+(i+1)*60)/360))*R
                    if (i == 0) {
                        hexagon_path = hexagon_path.concat([x1+cx, y1+cy])
                    }
                    hexagon_path = hexagon_path.concat(['L', x2+cx, y2+cy])
                }
                hexagon_path.push('z')
                return paper.path(hexagon_path).attr(attr.edge)
            }

        }

        var $tryit;
        var io = new extIO({
            multipleArguments: false,
            functions: {
                python: 'hexagonal_islands',
                js: 'hexagonalIslands'
            },
            animation: function($expl, data){
                hexagonalIslandsCanvas(
                    $expl[0],
                    data,
                );
            }
        });
        io.start();
    }
);
