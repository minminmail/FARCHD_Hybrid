# This file is part of KEEL-software, the Data Mining tool for regression,
# classification, clustering, pattern mining and so on.
#
# Copyright (C) 2004-2010
#
# F. Herrera (herrera@decsai.ugr.es)

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

# * <p>Title: Cover</p>
# * <p>Description: This class contains the representation to examples covered</p>
# * <p>Copyright: Copyright KEEL (c) 2007</p>
# * <p>Company: KEEL </p>
# * @author Written by Jesus Alcala (University of Granada) 09/02/2011
# * @version 1.0
# * @since JDK1.6
# */
class Cover:
    # int
    pos = None

    # /**
    #  * Parameter constructor.
    #  * @param pos position of the covered example.
    #  */

    def __init__(self, pos):
        self.pos = pos

    # * Returns a copy of the Cover object.
    # * @return Copy of the Cover object.

    def clone(self):
        return Cover(self.pos)

    # * Returns the position of the covered example.
    # * @return position of the covered example.

    def get_pos(self):
        return self.pos
