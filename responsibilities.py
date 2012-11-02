# coding: utf-8
#
# Copyright © 2012 Ejwa Software. All rights reserved.
#
# This file is part of gitinspector.
#
# gitinspector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gitinspector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gitinspector. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import blame
import terminal
import textwrap

class ResponsibiltyEntry:
	blames = {}

class Responsibilities:
	@staticmethod
	def get(hard, author_name):
		author_blames = {}

		for i in blame.get(hard).blames.items():
			if (author_name == i[0][0]):
				total_rows = i[1].rows - i[1].comments
				if total_rows > 0:
					author_blames[i[0][1]] = total_rows

		return sorted(author_blames.items())

__responsibilities_info_text__ = ("The following repsonsibilties, by author, were found in the current "
                                  "revision of the repository (comments are exluded from the line count, "
                                  "if possible)")
def output_html(hard):
	print("HTML output not yet supported.")

def output_text(hard):
	print("\n" + textwrap.fill(__responsibilities_info_text__ + ":", width=terminal.get_size()[0]))

	for i in sorted(set(i[0] for i in blame.get(hard).blames)):
		print("\n" + i, "is mostly responsible for:")
		responsibilities = sorted(((i[1], i[0]) for i in Responsibilities.get(hard, i)), reverse=True)

		for j, entry in enumerate(responsibilities):
			(width, _) = terminal.get_size()
			width -= 7

			print(str(entry[0]).rjust(6), end=" ")
			print("...%s" % entry[1][-width+3:] if len(entry[1]) > width else entry[1])

			if j >= 9:
				break

def output_xml(hard):
	message_xml = "\t\t<message>" + __responsibilities_info_text__ + "</message>\n"
	resp_xml = ""

	for i in sorted(set(i[0] for i in blame.get(hard).blames)):
		resp_xml += "\t\t\t<author>\n"
		resp_xml += "\t\t\t\t<name>" + i + "</name>\n"
		resp_xml += "\t\t\t\t<files>\n"
		responsibilities = sorted(((i[1], i[0]) for i in Responsibilities.get(hard, i)), reverse=True)

		for j, entry in enumerate(responsibilities):
			resp_xml += "\t\t\t\t\t<file>\n"
			resp_xml += "\t\t\t\t\t\t<name>" + entry[1] + "</name>\n"
			resp_xml += "\t\t\t\t\t\t<rows>" + str(entry[0]) + "</rows>\n"
			resp_xml += "\t\t\t\t\t</file>\n"

		resp_xml += "\t\t\t\t</files>\n"
		resp_xml += "\t\t\t</author>\n"

	print("\t<responsibilities>\n" + message_xml + "\t\t<authors>\n" + resp_xml + "\t\t</authors>\n\t</responsibilities>")
