What is it?

Blendxus is an add-on for Blender 3D (blender.org), which is used for creating new edges between near vertices. 

It is inspired by the ‘Creating Geometry with Vex’ Tutorial by Entagma:
http://www.entagma.com/creating-geometry-with-vex/
And by the famous ‘Plexus’ add on for after effects.

It was written by Christopher Kopic in August 2017.

Installing the addon:

1.	Download the .zip file.
2.	Unpack it somewhere on your hard drive
3.	In Blender open the user preferences, navigate to the addons tab and click ‚Install Add-on from File‘
4.	Select the ‘blendxus.py’ file in your extracted and click ‚Install Add-on from File…‘
5.	Select the checkbox next to ‚Mesh: Fractal Poke‘ and click ‚Safe User Settings‘

Using the operator:

The operator works with every mesh object, which has at least two vertices. To use it, in Object Mode, hit space, type ‚Blendxus‘and hit enter. Your object should change immediately and you are presented with four parameters, you can tweak:
-	Maximum Connections: The maximum number of connections per vertex.
-	Maximum Distance: The maximum distance between two verts for creating a connection.
-	Delete Initial Edges and Faces: This deletes all existing edges and faces to make the new connections visible.
-	Export to Curve: This converts the edgenet to curves for rendering. The effect won't be editable afterwards.

