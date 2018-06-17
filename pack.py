import sys


class Rect:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Pack:
    w = 0
    h = 0
    allow_rotations = False
    used_rectangles = []
    free_rectangles = []

    def __init__(self, w, h, rotations=True):
        self.init(w, h, rotations)

    def init(self, w, h, rotations=True):
        self.w = w
        self.h = h
        self.allow_rotations = rotations

        self.used_rectangles.clear()
        self.free_rectangles.clear()
        self.free_rectangles.append(Rect(0, 0, w, h))

    def insert(self, w, h):
        new_node, score1, score2 = self._find_position(w, h)

        if new_node.h == 0:
            return new_node

        num_rectangles_to_process = len(self.free_rectangles)
        i = 0

        while i < num_rectangles_to_process:
            if self._split_free_node(self.free_rectangles[i], new_node):
                self.free_rectangles.pop(i)
                i -= 1
                num_rectangles_to_process -= 1
            i += 1

        self._prune_free_list()
        self.used_rectangles.append(new_node)

        return new_node

    def _find_position(self, w, h):
        best_node = Rect()
        best_area_fit = sys.maxsize
        best_short_side_fit = 0

        for rect in self.free_rectangles:
            area_fit = rect.w * rect.h - w * h

            if rect.w >= w and rect.h >= h:
                left_over_horiz = abs(rect.w - w)
                left_over_vert = abs(rect.h - h)
                short_side_fit = min(left_over_horiz, left_over_vert)

                if area_fit < best_area_fit or (area_fit == best_area_fit and short_side_fit < best_short_side_fit):
                    best_node.x = rect.x
                    best_node.y = rect.y
                    best_node.w = w
                    best_node.h = h
                    best_short_side_fit = short_side_fit
                    best_area_fit = area_fit

            if self.allow_rotations and rect.w >= h and rect.h >= w:
                left_over_horiz = abs(rect.w - h)
                left_over_vert = abs(rect.h - w)
                short_side_fit = min(left_over_horiz, left_over_vert)

                if area_fit < best_area_fit or (area_fit == best_area_fit and short_side_fit < best_short_side_fit):
                    best_node.x = rect.x
                    best_node.y = rect.y
                    best_node.w = h
                    best_node.h = w
                    best_short_side_fit = short_side_fit
                    best_area_fit = area_fit

        return best_node, best_area_fit, best_short_side_fit

    def _split_free_node(self, free_node: Rect, used_node: Rect):
        if used_node.x >= free_node.x + free_node.w or used_node.x + used_node.w <= free_node.x \
                or used_node.y >= free_node.y + free_node.h or used_node.y + used_node.h <= free_node.y:
            return False

        if used_node.x < free_node.x + free_node.w and used_node.x + used_node.w > free_node.x:
            if used_node.y > free_node.y and used_node.y < free_node.y + free_node.h:
                new_node = Rect(free_node.x, free_node.y, free_node.w, used_node.y - free_node.y)
                self.free_rectangles.append(new_node)

            if used_node.y + used_node.h < free_node.y + free_node.h:
                h = free_node.y + free_node.h - (used_node.y + used_node.h)
                new_node = Rect(free_node.x, used_node.y + used_node.h, free_node.w, h)
                self.free_rectangles.append(new_node)

        if used_node.y < free_node.y + free_node.h and used_node.y + used_node.h > free_node.y:
            if used_node.x > free_node.x and used_node.x < free_node.x + free_node.w:
                new_node = Rect(free_node.x, free_node.y, used_node.x - free_node.x, free_node.h)
                self.free_rectangles.append(new_node)

            if used_node.x + used_node.w < free_node.x + free_node.w:
                w = free_node.x + free_node.w - (used_node.x + used_node.w)
                new_node = Rect(used_node.x + used_node.w, free_node.y, w, free_node.h)
                self.free_rectangles.append(new_node)

        return True

    def _prune_free_list(self):
        i = 0

        while i < len(self.free_rectangles):
            j = i + 1

            while j < len(self.free_rectangles):
                if self._is_contained_in(self.free_rectangles[i], self.free_rectangles[j]):
                    self.free_rectangles.pop(i)
                    i -= 1
                    break

                if self._is_contained_in(self.free_rectangles[j], self.free_rectangles[i]):
                    self.free_rectangles.pop(j)
                    j -= 1

                j += 1

            i += 1


    @staticmethod
    def _is_contained_in(a: Rect, b:Rect):
        return a.x >= b.x and a.y >= b.y and a.x + a.w <= b.x + b.w and a.y + a.h <= b.y + b.h

