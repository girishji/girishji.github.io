import pcbnew

# import math
from pcbnew import wxPoint, wxPointMM

#
# # Footprints
# board = pcbnew.GetBoard()
# r1 = board.FindFootprintByReference("R1")
# r2 = board.FindFootprintByReference("R2")
# d1 = board.FindFootprintByReference("D1")
# assert(r1 and r2 and d1)
#
# # Place footprints
# r1.SetPosition(wxPointMM(20, 20))
# r1.SetOrientation(90 * 10)
# r2.SetPosition(wxPointMM(25, 21))
# d1.SetPosition(wxPointMM(23, 26))
#

# def add_track(start, end, layer=pcbnew.F_Cu):
#     board = pcbnew.GetBoard()
#     track = pcbnew.PCB_TRACK(board)
#     track.SetStart(start)
#     track.SetEnd(end)
#     track.SetWidth(int(0.25 * 1e6))
#     track.SetLayer(layer)
#     board.Add(track)
#
#
# # Route track from pad #1 of footprint R1 to pad #1 of D1 with 45-deg corner
# start = board.FindFootprintByReference("R1").FindPadByNumber("1").GetCenter()
# end = board.FindFootprintByReference("D1").FindPadByNumber("1").GetCenter()
# offset = end.x - start.x
# thru = pcbnew.wxPoint(start.x, end.y - offset)
# add_track(start, thru)
# add_track(thru, end)

#
# def add_track_arc(start, mid, end, layer=pcbnew.F_Cu):
#     board = pcbnew.GetBoard()
#     track = pcbnew.PCB_ARC(board)
#     track.SetStart(start)
#     track.SetMid(mid)
#     track.SetEnd(end)
#     track.SetWidth(int(0.25 * 1e6))
#     track.SetLayer(layer)
#     board.Add(track)
#
#
# # for t in board.GetTracks():
# #     board.Delete(t)
#
# # Route track from pad #2 of footprint R1 to pad #1 of R2
# #   with 90-deg arc of radius 1.5mm
# board = pcbnew.GetBoard()
# radius = 1.5 * pcbnew.IU_PER_MM
# start = board.FindFootprintByReference("R1").FindPadByNumber("2").GetCenter()
# end = board.FindFootprintByReference("R2").FindPadByNumber("1").GetCenter()
# start1 = pcbnew.wxPoint(end.x - radius, start.y)
# add_track(start, start1)
# end1 = pcbnew.wxPoint(end.x, start.y + radius)
# add_track(end1, end)
# # Find the mid point of the arc by translating the origin to the center of arc
# #   and rotating the axis by 45-deg
# theta = 45
# mid = wxPoint(
#     start1.x + radius * math.cos(math.radians(theta)),
#     end1.y - radius * math.sin(math.radians(theta)),
# )
# add_track_arc(start1, mid, end1)
#

# # Create a via at 1mm offset from pad #2 of R2 and connect a track to it
# board = pcbnew.GetBoard()
# pad = board.FindFootprintByReference("R2").FindPadByNumber("2").GetCenter()
# via_location = wxPoint(pad.x + 1 * pcbnew.IU_PER_MM, pad.y)
# add_track(pad, via_location)
# via = pcbnew.PCB_VIA(board)
# via.SetPosition(via_location)
# via.SetDrill(int(0.4 * 1e6))
# via.SetWidth(int(0.8 * 1e6))
# board.Add(via)
#

# def add_line(start, end, layer=pcbnew.Edge_Cuts):
#     board = pcbnew.GetBoard()
#     segment = pcbnew.PCB_SHAPE(board)
#     segment.SetShape(pcbnew.SHAPE_T_SEGMENT)
#     segment.SetStart(start)
#     segment.SetEnd(end)
#     segment.SetLayer(layer)
#     segment.SetWidth(int(0.1 * pcbnew.IU_PER_MM))
#     board.Add(segment)
#
#
# for dr in board.GetDrawings():
#     board.Delete(dr)
#
# # Create a border for pcb in Edge Cuts layer
# # border = {"top": 3, "right": 5, "bottom": 4, "left": 4}
# # border = {side: val * pcbnew.IU_PER_MM for side, val in border.items()}
# border = 4 * pcbnew.IU_PER_MM
# radius = 1 * pcbnew.IU_PER_MM
# r1 = board.FindFootprintByReference("R1").GetPosition()
# r2 = board.FindFootprintByReference("R2").GetPosition()
# d1 = board.FindFootprintByReference("D1").GetPosition()
# start = wxPoint(r1.x - border + radius, r1.y - border)
# end = wxPoint(r2.x + border - radius, r1.y - border)
# add_line(start, end)
# start = wxPoint(end.x + radius, end.y + radius)
# end = wxPoint(start.x, d1.y + border - radius)
# add_line(start, end)
# start = wxPoint(end.x - radius, end.y + radius)
# end = wxPoint(r1.x - border + radius, start.y)
# add_line(start, end)
# start = wxPoint(end.x - radius, end.y - radius)
# end = wxPoint(start.x, r1.x - border + radius)
# add_line(start, end)
#


def add_line_arc(start, center, angle=90, layer=pcbnew.Edge_Cuts):
    board = pcbnew.GetBoard()
    arc = pcbnew.PCB_SHAPE(board)
    arc.SetShape(pcbnew.SHAPE_T_ARC)
    arc.SetStart(start)
    arc.SetCenter(center)
    arc.SetArcAngleAndEnd(angle * 10, False)
    arc.SetLayer(layer)
    arc.SetWidth(int(0.1 * pcbnew.IU_PER_MM))
    board.Add(arc)


board = pcbnew.GetBoard()
border = 4 * pcbnew.IU_PER_MM
radius = 1 * pcbnew.IU_PER_MM
r1 = board.FindFootprintByReference("R1").GetPosition()
r2 = board.FindFootprintByReference("R2").GetPosition()
d1 = board.FindFootprintByReference("D1").GetPosition()
start = wxPoint(r2.x + border - radius, r1.y - border)
center = wxPoint(start.x, start.y + radius)
add_line_arc(start, center)
start = wxPoint(start.x + radius, d1.y + border - radius)
center = wxPoint(start.x - radius, start.y)
add_line_arc(start, center)
start = wxPoint(r1.x - border + radius, start.y + radius)
center = wxPoint(start.x, start.y - radius)
add_line_arc(start, center)
start = wxPoint(start.x - radius, r1.y - border + radius)
center = wxPoint(start.x + radius, start.y)
add_line_arc(start, center)


pcbnew.Refresh()
