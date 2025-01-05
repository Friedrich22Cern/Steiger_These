;; Author: Nikita Steiger
;;
;;                                             THE DYNAMICS OF INFORMATION
;;
;;
;;---------------------------------------------------------------------------------------------------------------------------
;;                                       INITIALISATION: GLOBALS, INDIVIDUALS & LINKS
;;---------------------------------------------------------------------------------------------------------------------------

GLOBALS [
  ;-----  RANDOMNESS  -------------------------------------------------------------------------------------------------------
  ; random-seed? (switch)                    ;; random-seed? True / False
  ; random-seed-value (slider)               ;; value for random-seed

  ;-----  NETWORK  ----------------------------------------------------------------------------------------------------------
  ; type-of-network (chooser)                ;; lets you choose the type of network: fully connected, 2, 3, 4, circle
  ; num-of-nodes (slider)                    ;; lets you choose the number of individuals (nodes) in the network
  ; source-reach (slider)                    ;; the number of individuals with a direct connection to the source of
                                             ;; information (seed nodes)
  ; rewiring-probability (slider)            ;; the probability or share of nodes to be rewired
  stabilised?                                ;; checks if the network dynamics are stable (0 infected individuals)
  infinity                                   ;; used to represent the distance between two nodes with no path between them
  number-rewired                             ;; number of rewired edges (used in the creation of the small world network)
  ; lower-limit-weight (slider)              ;; sets the lower limit on the tie strength
  ; upper-limit-weight (slider)              ;; sets the upper limit on the tie strength (weight becomes a random value
                                             ;; between the lower and the upper limit)
  ; uniform-weight (slider)                  ;; weight given to all links when uniform-weight? is true
  ; uniform-weight? (switch)                 ;; true/false - determines if all links are given equal weight (On) or randomly
                                             ;; varied (Off)

  ;-----  STATISTICS  -------------------------------------------------------------------------------------------------------
  clustering-coefficient                     ;; the clustering coefficient of the current network (important small world
                                             ;; property)
  average-path-length                        ;; the average distance between individuals (important small world property)
  informed-individuals                       ;; the absolute number of informed individuals
  share-of-informed-individuals              ;; the relative share of informed individuals (in case number of individuals in
                                             ;; the model (num-of-nodes) deviates from 100)
  infected-individuals                       ;; the number of infected individuals
  average-degree                             ;; the average degree across all nodes
  transmission-rate                          ;; the transmission rate at time t (amount of information transmissions/"in-
                                             ;; fections" in the current tick)
  total-transmissions                        ;; cumulative number of transmissions across all ticks
  avg-transmission-rate                      ;; the average transmission rate across the whole cycle (after stabilisation)
  num-ticks                                  ;; number of ticks that have elapsed
];; GLOBALS

breed [ individuals individual ]
individuals-own [
  diffusion-state                            ;; diffusion state of the individual: susceptible, infected, recovered
  distance-from-other-individuals            ;; list of distances of this node from other nodes/individuals
  local-clustering-coefficient               ;; the clustering coefficient of this node
  my-angle                                   ;; for the creation of the star and royal family networks, each peripheral node
                                             ;; is assigned an angle during the circular placement
];; individuals-own

links-own [
  weight                                     ;; stores the weight of the tie connecting two nodes
];; links-own

;;---------------------------------------------------------------------------------------------------------------------------
;;                                                       SETUP
;;---------------------------------------------------------------------------------------------------------------------------

; The following procedure connects nodes through edges
to MAKE-EDGE [ node-A node-B the-shape ]
  ask node-A [
    create-link-with node-B  [
      set shape the-shape
      ifelse ( uniform-weight? = false ) [ ; if weight is varied, set the weight randomly to a value between the upper
                                           ; and lower limit on the weight
        set weight random-float ( ( upper-limit-weight + 0.000001 ) - lower-limit-weight ) + lower-limit-weight
                                                                  ; Assign a random weight between lower-limit-weight
                                                                  ; (slider) and upper-limit-weight (slider) as the tie
                                                                  ; strength. The additional increment on the upper limit
                                                                  ; is needed because random-float apparently does not
                                                                  ; include the upper bound.
      ] [ ; if weight is uniform, set the weight of all edges to the same value chosen by the slider
        set weight uniform-weight
      ]
    ]
  ]
end;; MAKE-EDGE

to CREATE-CIRCLE-NETWORK
  ; create connections:
  ; successively make edges with the next neighbour
  let n 0
  while [ n < count individuals ] [
    MAKE-EDGE individual n
    individual ((n + 1) mod count individuals)
    "default"
    set n n + 1
  ]
  ; seed nodes setup: the individuals with a direct link to the source are infected from the start
  ask n-of source-reach individuals [
    set diffusion-state "infected"
  ]
end;; CREATE-CIRCLE-NETWORK

to CREATE-FULLY-CONNECTED-NETWORK
  ; every individual successively makes connection with every other individual
  ask individuals [
    let node-A self
    ask other individuals [
      let node-B self
      if not link-neighbor? node-B [
        MAKE-EDGE node-A node-B "default"
      ]
    ]
  ]
  ; seed nodes setup: the individuals with a direct link to the source are infected from the start
  ask n-of source-reach individuals [
    set diffusion-state "infected"
  ]
end;; CREATE-FULLY-CONNECTED-NETWORK

to CREATE-SMALL-WORLD-NETWORK
  ; FROM MODEL LIBRARY; ADJUSTED
  ; A rewiring probability of around 0.08 leads to the small-world properties, i.e., an average path length of 5-6 and
  ; a clustering coefficient of 0.1-0.5.
  let n 0
  while [ n < count individuals ] [
    ; make edges with the next two neighbors
    ; this makes a lattice with average degree of 4
    make-edge individual n
    individual ((n + 1) mod count individuals)
    "default"
    ; Make the neighbor's neighbor links curved
    make-edge individual n
    individual ((n + 2) mod count individuals)
    "curve"
    set n n + 1
  ]
  ; A share of [rewiring-probability] individuals is asked to rewire one of its edges to a random other individual to
  ; create the small-world network.
  ask links [
    if (random-float 1) < rewiring-probability [ rewire-me ]
  ]
  ; seed nodes setup: the individuals with a direct link to the source are infected from the start
  ask n-of source-reach individuals [
    set diffusion-state "infected"
  ]
end;; CREATE-SMALL-WORLD-NETWORK

; (FROM MODEL LIBRARY; adjusted:)
to REWIRE-ME
  ; this is a procedure used by individuals
  ; node-A remains the same
  let node-A end1
  ; as long as A is not connected to everybody
  if [ count link-neighbors ] of end1 < (count individuals - 1) [
    ; find a node distinct from A and not already a neighbor of A
    let node-B one-of individuals with [ (self != node-A) and (not link-neighbor? node-A) ]
    ; wire the new edge
    MAKE-EDGE node-A node-B "default"
    set number-rewired number-rewired + 1
    die ; remove the old edge
  ]
end;; REWIRE-ME

to CREATE-STAR-NETWORK
  ; Select the central node
  let central-node one-of individuals
  ask central-node [
    ; Make it visually distinct
    set size 1 ; Make it larger than other nodes
    set shape "star" ; Change shape to star
    set color yellow ; Make it yellow
    setxy 0 0 ; Place it in the center
  ]
  ; Get the list of peripheral nodes
  let peripheral-nodes individuals with [self != central-node]

  ; Arrange peripheral nodes in a circle around the center
  let radius (max-pxcor - 1)  ; Use the same radius as in the circle layout
  let num-nodes count peripheral-nodes
  let angle 360 / num-nodes
  let current-angle 0

  ; Store each node's angle to ensure proper ordering
  ask peripheral-nodes [
    ; Position each node in a circle around the center
    setxy (radius * cos current-angle) (radius * sin current-angle)
    set my-angle current-angle
    set current-angle current-angle + angle
  ]

  ; Connect central node to all peripheral nodes
  ask peripheral-nodes [
    MAKE-EDGE self central-node "default"
  ]

  ; Sort peripheral nodes by the angle they were placed at
  let ordered-nodes sort-by [ [a b] -> [my-angle] of a < [my-angle] of b ] peripheral-nodes

  ; Connect each node to its immediate neighbors in the circle
  let i 0
  while [i < length ordered-nodes] [
    let current-node item i ordered-nodes
    let next-node item ((i + 1) mod length ordered-nodes) ordered-nodes
    MAKE-EDGE current-node next-node "default"
    set i i + 1
  ]
  ; seed nodes setup: the individuals with a direct link to the source are infected from the start
  ask n-of source-reach individuals [
    set diffusion-state "infected"
  ]
end;; CREATE-STAR-NETWORK

to CREATE-ROYAL-FAMILY-NETWORK
  ; In this network, the central node is always the seed node
  ; Select the central node
  let central-node one-of individuals
  ask central-node [
    ; Make it visually distinct
    set size 1 ; Make it larger than other nodes
    set shape "star" ; Change shape to star
    set color yellow ; Make it yellow
    setxy 0 0 ; Place it in the center
  ]

  ; Get the list of peripheral nodes
  let peripheral-nodes individuals with [self != central-node]

  ; Arrange peripheral nodes in a circle around the center
  let radius (max-pxcor - 1)  ; Use the same radius as in the circle layout
  let num-nodes count peripheral-nodes
  let angle 360 / num-nodes
  let current-angle 0

  ; Store each node's angle to ensure proper ordering
  ask peripheral-nodes [
    ; Position each node in a circle around the center
    setxy (radius * cos current-angle) (radius * sin current-angle)
    set my-angle current-angle
    set current-angle current-angle + angle
  ]

  ; Connect central node to all peripheral nodes
  ask peripheral-nodes [
    MAKE-EDGE self central-node "default"
  ]

  ; Sort peripheral nodes by the angle they were placed at
  let ordered-nodes sort-by [ [a b] -> [my-angle] of a < [my-angle] of b ] peripheral-nodes

  ; Connect each node to its immediate neighbors in the circle
  let i 0
  while [i < length ordered-nodes] [
    let current-node item i ordered-nodes
    let next-node item ((i + 1) mod length ordered-nodes) ordered-nodes
    MAKE-EDGE current-node next-node "default"
    set i i + 1
  ]
  ; seed nodes setup: the individuals with a direct link to the source are infected from the start
  ask central-node [
    set diffusion-state "infected"
  ]
end;; CREATE-ROYAL-FAMILY-NETWORK

to CREATE-NETWORK
  ; create the nodes and arrange them in a circle
  set-default-shape individuals "circle"
  create-individuals num-of-nodes [ set color gray ]
  layout-circle ( sort individuals ) max-pxcor - 1
  ask individuals [
    set size 0.5
    set diffusion-state "susceptible" ; Each individual is susceptible from the start except for the seed nodes. The
                                      ; seed nodes are managed at the end of the setup of each network type.
  ]
  ; The correct network will be created based on the selection in the chooser on the interface
  ;--------------- network: circle ------------------------------------------------------------------------------------------
  if type-of-network = "circle" [
    CREATE-CIRCLE-NETWORK
  ]

  ;--------------- network: fully connected/complete graph ------------------------------------------------------------------
  if type-of-network = "fully connected" [
    CREATE-FULLY-CONNECTED-NETWORK
  ]

  ;--------------- network: small world -------------------------------------------------------------------------------------
  if type-of-network = "small world" [
    CREATE-SMALL-WORLD-NETWORK
  ]

  ;--------------- network: star --------------------------------------------------------------------------------------------
  if type-of-network = "star" [
    CREATE-STAR-NETWORK
  ]

  ;--------------- network: royal family ------------------------------------------------------------------------------------
  if type-of-network = "royal family" [
    CREATE-ROYAL-FAMILY-NETWORK
  ]
  ask links [
    set color scale-color blue weight 0 1 ; Scales blue intensity based on weight (the larger the weight, the lighter the
                                          ; blue colour of the edge)
  ]
end;; CREATE-NETWORK

to SETUP
  clear-all
  reset-ticks
  set infinity 99999 ; this is an arbitrary choice for a large number
  set num-ticks 0
  ifelse ( random-seed? = true )
    [ random-seed random-seed-value ]
    [ random-seed new-seed ]
  CREATE-NETWORK
  UPDATE-VISUALS
  DO-STATISTICS
end;; SETUP

;;---------------------------------------------------------------------------------------------------------------------------
;;                                                      DYNAMICS
;;---------------------------------------------------------------------------------------------------------------------------

to GO
  tick
  RUN-DIFFUSION
  UPDATE-VISUALS
  DO-STATISTICS
  CHECK-STABILISATION
  if stabilised? = true [ stop ]
end;; GO

to RUN-DIFFUSION
  let new-infections 0 ; Initialize counter for new infections this tick
  ask individuals with [ diffusion-state = "infected" ] [
    ask my-links [
      let neighbour other-end
      if [ diffusion-state ] of neighbour = "susceptible" [
        if random-float 1 < weight [ ;; with a probability of [weight], the neighbour becomes infected
          ask neighbour [
            set diffusion-state "infected"
            set new-infections new-infections + 1 ; Increment counter when infection occurs
          ]
        ]
      ]
    ]
    set diffusion-state "recovered"
  ]
  ; Update transmission statistics
  set transmission-rate new-infections ; Store this tick's transmission count
  set total-transmissions total-transmissions + new-infections ; Add to cumulative total
  set num-ticks num-ticks + 1 ; Increment tick counter
end;; RUN-DIFFUSION

to UPDATE-VISUALS
  ask individuals with [ diffusion-state = "infected" ] [
    set color red
  ]
  ask individuals with [ diffusion-state = "recovered" ] [
    set color green
  ]
end;; UPDATE-VISUALS

to CHECK-STABILISATION
  ;; As soon as there are no infected individuals, the network is stable
  set infected-individuals ( count individuals with [ diffusion-state = "infected" ] )
  if infected-individuals = 0 [
    set stabilised? true
  ]
end;; CHECK-STABILISATION

;;---------------------------------------------------------------------------------------------------------------------------
;;                                                      STATISTICS
;;---------------------------------------------------------------------------------------------------------------------------

; (FROM MODEL LIBRARY; adjusted:) Implements the Floyd Warshall algorithm for All Pairs Shortest Paths. It is a dynamic
; programming algorithm which builds bigger solutions from the solutions of smaller subproblems using memorisation that
; is storing the results. It keeps finding incrementally if there is a shorter path through the kth node. Since it
; iterates over all turtles through k, at the end we get the shortest possible path for each i and j.
to FIND-PATH-LENGTHS
  ; reset the distance list
  ask individuals [
    set distance-from-other-individuals []
  ]

  let i 0
  let j 0
  let k 0
  let node1 one-of individuals
  let node2 one-of individuals
  let node-count count individuals
  ; initialize the distance lists
  while [i < node-count] [
    set j 0
    while [ j < node-count ] [
      set node1 individual i
      set node2 individual j
      ; zero from a node to itself
      ifelse i = j [
        ask node1 [
          set distance-from-other-individuals lput 0 distance-from-other-individuals
        ]
      ] [
        ; 1 from a node to it's neighbor
        ifelse [ link-neighbor? node1 ] of node2 [
          ask node1 [
            set distance-from-other-individuals lput 1 distance-from-other-individuals
          ]
        ][ ; infinite to everyone else
          ask node1 [
            set distance-from-other-individuals lput infinity distance-from-other-individuals
          ]
        ]
      ]
      set j j + 1
    ]
    set i i + 1
  ]
  set i 0
  set j 0
  let dummy 0
  while [k < node-count] [
    set i 0
    while [i < node-count] [
      set j 0
      while [j < node-count] [
        ; alternate path length through kth node
        set dummy ( (item k [distance-from-other-individuals] of turtle i) +
                    (item j [distance-from-other-individuals] of turtle k))
        ; is the alternate path shorter?
        if dummy < (item j [distance-from-other-individuals] of turtle i) [
          ask turtle i [
            set distance-from-other-individuals replace-item j distance-from-other-individuals dummy
          ]
        ]
        set j j + 1
      ]
      set i i + 1
    ]
    set k k + 1
  ]
end;; FIND-PATH-LENGTHS

; (FROM MODEL LIBRARY - but omitted connectivity check because I know that the network is connected)
; Procedure to calculate the average-path-length (apl) in the network.
to-report FIND-AVERAGE-PATH-LENGTH
  let apl 0
  ; calculate all the path-lengths for each node
  find-path-lengths
  let num-connected-pairs sum [length remove infinity (remove 0 distance-from-other-individuals)] of individuals
  ; Calculate the average path length
  set apl (sum [sum distance-from-other-individuals] of individuals) / num-connected-pairs
  report apl
end;; FIND-AVERAGE-PATH-LENGTH

; (FROM MODEL LIBRARY) Used in FIND-CLUSTERING-COEFFICIENT
to-report in-neighborhood? [ hood ]
  report ( member? end1 hood and member? end2 hood )
end;; in-neighborhood?

to-report FIND-CLUSTERING-COEFFICIENT
  let cc infinity
  ifelse all? individuals [ count link-neighbors <= 1 ] [
    ; it is undefined
    ; what should this be?
    set cc 0
  ][
    let total 0
    ask individuals with [ count link-neighbors <= 1 ] [ set local-clustering-coefficient "undefined" ]
    ask individuals with [ count link-neighbors > 1 ] [
      let hood link-neighbors
      set local-clustering-coefficient (2 * count links with [ in-neighborhood? hood ] /
                                         ((count hood) * (count hood - 1)) )
      ; find the sum for the value at turtles
      set total total + local-clustering-coefficient
    ]
    ; take the average
    set cc total / count individuals with [count link-neighbors > 1]
  ]
  report cc
end;; FIND-CLUSTERING-COEFFICIENT

to-report REPORT-INFORMED-INDIVIDUALS
  ; counts the number of informed individuals, which is those who are currently infected or already recovered
  report count individuals with [ diffusion-state = "infected" or diffusion-state = "recovered" ]
end;; REPORT-INFORMED-INDIVIDUALS

to-report REPORT-SHARE-INFORMED-INDIVIDUALS
  ; reports the relative share of informed individuals
  report count individuals with [ diffusion-state = "infected" or diffusion-state = "recovered" ] / num-of-nodes
end;; REPORT-SHARE-INFORMED-INDIVIDUALS

to-report REPORT-AVERAGE-DEGREE
  ; counts and sums the number of edges of all individuals
  let total-degree 0
    ask individuals [
      set total-degree total-degree + count my-links
    ]
  ; reports the average degree
  report total-degree / count individuals
end;; REPORT-AVERAGE-DEGREE

to-report REPORT-TRANSMISSION-RATE
  report transmission-rate
end;; REPORT-TRANSMISSION-RATE

to-report REPORT-AVERAGE-TRANSMISSION-RATE
  ; counts the cumulative number of transmissions, divided by the number of ticks (a proxy for time)
  ifelse num-ticks > 0 [
    report total-transmissions / num-ticks
  ] [
    report 0
  ]
end;; REPORT-AVERAGE-TRANSMISSION-RATE

to DO-STATISTICS
  set average-path-length FIND-AVERAGE-PATH-LENGTH
  set clustering-coefficient FIND-CLUSTERING-COEFFICIENT
  set informed-individuals REPORT-INFORMED-INDIVIDUALS
  set share-of-informed-individuals REPORT-SHARE-INFORMED-INDIVIDUALS
  set average-degree REPORT-AVERAGE-DEGREE
  set transmission-rate REPORT-TRANSMISSION-RATE
  set avg-transmission-rate REPORT-AVERAGE-TRANSMISSION-RATE
end;; DO-STATISTICS
@#$#@#$#@
GRAPHICS-WINDOW
361
10
873
523
-1
-1
15.3
1
10
1
1
1
0
0
0
1
-16
16
-16
16
0
0
1
ticks
30.0

CHOOSER
27
131
166
176
type-of-network
type-of-network
"circle" "royal family" "small world" "star" "fully connected"
4

BUTTON
60
16
125
50
Setup
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
134
16
214
50
Go Once
GO
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
220
16
284
50
Go
GO
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
171
118
324
151
num-of-nodes
num-of-nodes
1
100
100.0
1
1
NIL
HORIZONTAL

SLIDER
171
157
324
190
source-reach
source-reach
0
num-of-nodes
0.0
1
1
NIL
HORIZONTAL

MONITOR
5
458
102
503
Avg. Path Length
average-path-length
4
1
11

MONITOR
120
458
235
503
Clustering Coefficient
clustering-coefficient
4
1
11

SLIDER
28
351
200
384
rewiring-probability
rewiring-probability
0
1
0.08
0.01
1
NIL
HORIZONTAL

MONITOR
203
579
359
624
Informed Individuals
informed-individuals
0
1
11

MONITOR
204
527
358
572
Share of Informed Individuals
share-of-informed-individuals
4
1
11

SLIDER
182
269
326
302
upper-limit-weight
upper-limit-weight
0
1
0.87
0.01
1
NIL
HORIZONTAL

SWITCH
42
57
166
90
random-seed?
random-seed?
1
1
-1000

SLIDER
172
57
310
90
random-seed-value
random-seed-value
0
100
50.0
1
1
NIL
HORIZONTAL

SWITCH
29
227
170
260
uniform-weight?
uniform-weight?
0
1
-1000

SLIDER
180
228
327
261
uniform-weight
uniform-weight
0
1
0.1
0.01
1
NIL
HORIZONTAL

SLIDER
29
270
170
303
lower-limit-weight
lower-limit-weight
0
1
0.3
0.01
1
NIL
HORIZONTAL

MONITOR
254
457
355
502
Avg. Node Degree
average-degree
5
1
11

PLOT
362
526
870
676
Informed Individuals
Time
Individuals
0.0
20.0
0.0
100.0
false
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "plot informed-individuals"

MONITOR
6
776
63
821
Time
ticks
0
1
11

PLOT
362
678
871
825
Transmission Rate
Time
Rate
0.0
20.0
0.0
70.0
false
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "plot transmission-rate"

MONITOR
206
731
356
776
Avg Transmission Rate
avg-transmission-rate
5
1
11

MONITOR
206
681
356
726
Current Transmission Rate
transmission-rate
5
1
11

TEXTBOX
158
804
308
822
The plot is delayed by one tick
11
0.0
1

TEXTBOX
41
386
191
404
Used in creation of small world
11
0.0
1

@#$#@#$#@
## WHAT IS IT?

(a general understanding of what the model is trying to show or explain)

## HOW IT WORKS

(what rules the agents use to create the overall behavior of the model)

## HOW TO USE IT

(how to use the model, including a description of each of the items in the Interface tab)

## THINGS TO NOTICE

(suggested things for the user to notice while running the model)

## THINGS TO TRY

(suggested things for the user to try to do (move sliders, switches, etc.) with the model)

## EXTENDING THE MODEL

(suggested things to add or change in the Code tab to make the model more complicated, detailed, accurate, etc.)

## NETLOGO FEATURES

(interesting or unusual features of NetLogo that the model uses, particularly in the Code tab; or where workarounds were needed for missing features)

## RELATED MODELS

(models in the NetLogo Models Library and elsewhere which are of related interest)

## CREDITS AND REFERENCES

(a reference to the model's URL on the web if it has one, as well as any other necessary credits, citations, and links)
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.4.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
<experiments>
  <experiment name="1" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="2" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
  </experiment>
  <experiment name="3" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.02"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="4" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.4"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="5" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="1 (postrun_commands)" repetitions="1" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <postRun>REPORT-AVERAGE-TRANSMISSION-RATE
REPORT-INFORMED-INDIVIDUALS</postRun>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="6" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="7" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="8" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.6"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="9" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="10" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="11" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="12" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="13" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="14" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="10"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="15" repetitions="100" sequentialRunOrder="false" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="30"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="16" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.6"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="17" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;royal family&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.6"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="18" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;royal family&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="19" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;royal family&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="20" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;royal family&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="21" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;royal family&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.6"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="22" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;royal family&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="23" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="24" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="25" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;royal family&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="26" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.87"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="27" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.87"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="28" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.87"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="29" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="30" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="31" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="32" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="20"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="33" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="1"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="34" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="5"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="35" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="10"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="36" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="30"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="37" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="38" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed-value">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.6"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="39" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="40" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="41" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="42" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="20"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="43" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="1"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="44" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="5"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="45" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="30"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="46" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="47" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.7"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="48" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="49" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="50" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="51" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="52" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.6"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="53" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="54" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="55" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.9"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="56" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="57" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.7"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="58" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.8"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="59" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="60" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="61" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0.3"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="0.6"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="62" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="63" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;fully connected&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="lower-limit-weight">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="upper-limit-weight">
      <value value="1"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="64" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="20"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="65" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="1"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="66" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="5"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="67" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="30"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="68" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="10"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="69" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="rewiring-probability">
      <value value="0.08"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;small world&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="70" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="10"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="71" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;star&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="72" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <steppedValueSet variable="source-reach" first="1" step="1" last="100"/>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight">
      <value value="0.7"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="73" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>FIND-AVERAGE-PATH-LENGTH</metric>
    <metric>FIND-CLUSTERING-COEFFICIENT</metric>
    <metric>REPORT-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-SHARE-INFORMED-INDIVIDUALS</metric>
    <metric>REPORT-AVERAGE-DEGREE</metric>
    <metric>REPORT-TRANSMISSION-RATE</metric>
    <metric>REPORT-AVERAGE-TRANSMISSION-RATE</metric>
    <enumeratedValueSet variable="num-of-nodes">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="uniform-weight?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="type-of-network">
      <value value="&quot;circle&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="source-reach">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="random-seed?">
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="uniform-weight" first="0.01" step="0.01" last="1"/>
  </experiment>
</experiments>
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180

curve
3.0
-0.2 0 0.0 1.0
0.0 0 0.0 1.0
0.2 1 1.0 0.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180

curve-a
-3.0
-0.2 0 0.0 1.0
0.0 0 0.0 1.0
0.2 1 1.0 0.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
