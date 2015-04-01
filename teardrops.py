#!/usr/bin/env python

# Teardrops for PCBNEW by svofski, 2014
# http://sensi.org/~svo

from pcbnew import *
from math import *

ToUnits=ToMM
FromUnits=FromMM

pcb = GetBoard()


def Line(p1, p2, w, layer):
	result = DRAWSEGMENT(None)
	result.SetStart(p1)
	result.SetEnd(p2)
	result.SetWidth(w)
	result.SetLayer(layer)
	return result

vias = []

for item in pcb.GetTracks():
    if type(item) == VIA:
        pos = item.GetPosition()
        drill = item.GetDrillValue()
        width = item.GetWidth()
        #print " * Via:   %s - %f/%f "%(ToUnits(pos),ToUnits(drill),ToUnits(width))
        vias.append((pos, width))

for i in xrange(pcb.GetPadCount()):
	pad = pcb.GetPad(i)
	if pad.GetAttribute() == PAD_STANDARD:
		if pad.GetDrillShape() == PAD_DRILL_CIRCLE:
		    vias.append((pad.GetPosition(), pad.GetDrillSize().x + FromUnits(0.2 * 2)))

		#print " * Through hole pad at: %s shape=%s" % (str(pad.GetPosition()), shape) 


count = 0
		
for track in pcb.GetTracks():
    if type(track) == TRACK:
        for via in vias:
        	if track.IsPointOnEnds(via[0], via[1]/2):
        		if track.GetLength() < via[1]:
        			continue

		        start = track.GetStart()
		        end = track.GetEnd()

		        # ensure that start is at the via/pad end
		        d = end - via[0]
		        if sqrt(d.x * d.x + d.y * d.y) < via[1]:
		        	start, end = end, start

		        # get normalized track vector
		        pt = end - start
		        norm = sqrt(pt.x * pt.x + pt.y * pt.y)
		        vec = [t / norm for t in pt]

		        # 2 pependicular vectors to find the end points on via side
		        vecB = [vec[1], - vec[0]]
		        vecC = [- vec[1], vec[0]]


		        # find point on the track, sharp end of the teardrop
		        dist = via[1] # if via[1]/width > 5.5 else via[1] * 0.85
		        pointA = start + wxPoint(int(vec[0] * dist), int(vec[1] * dist))

		        width = track.GetWidth()
		        radius = via[1] / 2  - width / 2
		        
		        # via side points
		        pointB = via[0] + wxPoint(int(vecB[0] * radius), int(vecB[1] * radius))
		        pointC = via[0] + wxPoint(int(vecC[0] * radius), int(vecC[1] * radius))

		        #print " * Viaful Track: %s to %s, width %f length %f" % (ToUnits(start),ToUnits(end),ToUnits(width), ToUnits(track.GetLength()))
		        # create the teardrop
		        pcb.Add(Line(pointA, pointB, width, track.GetLayer()))
		        pcb.Add(Line(pointA, pointC, width, track.GetLayer()))

		        # add extra lines if via/track ratio is high
		        if via[1]/width > 5.5:
		            radius = radius - width
		            pointB = via[0] + wxPoint(int(vecB[0] * radius), int(vecB[1] * radius))
		            pointC = via[0] + wxPoint(int(vecC[0] * radius), int(vecC[1] * radius))
		            pcb.Add(Line(pointA, pointB, width, track.GetLayer()))
		            pcb.Add(Line(pointA, pointC, width, track.GetLayer()))


		        count = count + 1


print "Teardrops generated for %d vias and pads. To undo, select all drawings in copper layers and delete block" % count
