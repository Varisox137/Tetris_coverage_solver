import turtle, random

UNIT=40
COLORS=[
    '#ff0000', # red
    '#cc6600', # brown
    '#ff9900', # orange
    '#ffff00', # yellow
    '#99ff33', # light green
    '#00cc00', # green
    '#00cc99', # cyan
    '#66ccff', # light blue
    '#0000ff', # blue
    '#cc66ff', # purple
    '#ff99cc', # pink
    '#ff3399', # rose
]
REL_POS={
    'I': (
        ((0,0),(0,1),(0,2),(0,3)),
        ((0,0),(1,0),(2,0),(3,0)),
    ),
    'J': (
        ((0,0),(0,1),(1,0),(2,0)),
        ((0,0),(0,1),(0,2),(1,2)),
        ((0,0),(1,0),(2,0),(2,-1)),
        ((0,0),(1,0),(1,1),(1,2)),
    ),
    'L': (
        ((0,0),(1,0),(2,0),(2,1)),
        ((0,0),(0,1),(0,2),(1,0)),
        ((0,0),(0,1),(1,1),(2,1)),
        ((0,0),(1,-2),(1,-1),(1,0)),
    ),
    'O': (
        ((0,0),(0,1),(1,0),(1,1)),
    ),
    'S': (
        ((0,0),(1,0),(1,1),(2,1)),
        ((0,0),(0,1),(1,-1),(1,0)),
    ),
    'T': (
        ((0,0),(0,1),(0,2),(1,1)),
        ((0,0),(1,-1),(1,0),(2,0)),
        ((0,0),(1,-1),(1,0),(1,1)),
        ((0,0),(1,0),(1,1),(2,0)),
    ),
    'Z': (
        ((0,0),(0,1),(1,1),(1,2)),
        ((0,0),(1,-1),(1,0),(2,-1)),
    )
}

class DancingLink:
    class Node:
        pos=(0,0)
        right,left,up,down=None,None,None,None
        col=None

        def set(self,pos=tuple(),col=None,r=None,l=None,u=None,d=None):
            if pos: self.pos=pos
            if col: self.col=col
            if r: self.right=r
            if l: self.left=l
            if u: self.up=u
            if d: self.down=d

    def __init__(self,source_matrix:list[list[int]]):
        # TO BE IMPROVED:
        # use global lists for direction pointers, instead of object attributes

        # row=len(mat); column=len(mat[0])
        # HEAD -> id=0, C_HEADs -> id=1~c
        # mat[0~r-1][0~c-1] -> id=c*(1~r)+(1~c)

        self.source=source_matrix
        self.column_count=len(source_matrix[0])
        self.row_count=0

        # init HEAD
        self.HEAD=self.Node()
        self.HEAD.set(pos=(0,0),col=self.HEAD,r=self.HEAD,l=self.HEAD,u=self.HEAD,d=self.HEAD)
        # add COLUMN_HEADs
        for i in range(self.column_count):
            last=self.HEAD.left
            c_head=self.Node()
            c_head.set(pos=(0,i+1),col=c_head,r=self.HEAD,l=last,u=c_head,d=c_head)
            last.set(r=c_head); self.HEAD.set(l=c_head)

    def append_row(self,row:list[int]):
        if 1 in row:
            self.row_count+=1
            # construct new DancingLink
            first=None
            column_head=self.HEAD
            for i in range(self.column_count):
                column_head=column_head.right
                if row[i]==1:
                    if not first:
                        first=self.Node()
                        first.set(pos=(self.row_count,i+1),col=column_head,r=first,l=first)
                    else:
                        last=first.left
                        new=self.Node()
                        new.set(pos=(self.row_count,i+1),col=column_head,r=first,l=last)
                        last.set(r=new); first.set(l=new)
            del i
            del column_head,last,new
            # link the new row-only Link to the whole DancingLink
            flag=None
            c_head=self.HEAD
            while flag!=first:
                if not flag: flag=first
                # find corresponding column
                while c_head.col!=flag.col: c_head=c_head.right
                # add link
                c_last=c_head.up
                flag.set(u=c_last,d=c_head); c_head.set(u=flag); c_last.set(d=flag)
                flag=flag.right

    @staticmethod
    def flag_column_head(c_head:Node):
        # remove column head
        c_head.right.set(l=c_head.left); c_head.left.set(r=c_head.right)
        # row-based order, row going down and column going right
        row_head=c_head.down
        while row_head!=c_head:
            row_next=row_head.right
            while row_next!=row_head:
                row_next.up.set(d=row_next.down); row_next.down.set(u=row_next.up)
                row_next=row_next.right
            row_head=row_head.down

    @staticmethod
    def unflag_column_head(c_head:Node):
        # restore column head
        c_head.right.set(l=c_head); c_head.left.set(r=c_head)
        # reverse order of the remove operation, row up and column left
        row_head=c_head.up
        while row_head!=c_head:
            row_back=row_head.left
            while row_back!=row_head:
                row_back.up.set(d=row_back); row_back.down.set(u=row_back)
                row_back=row_back.left
            row_head=row_head.up

    @classmethod
    def from_matrix(cls,mat:list[list[int]]):
        res=cls(mat)
        for r in mat:
            res.append_row(r)
        return res

def get_tetris_count() -> dict:
    counts=dict.fromkeys(['I','J','L','O','S','T','Z'],0)
    for shape in counts:
        counts[shape]=int(input(f'Number of {shape}-shaped tetris ?= '))
        assert counts[shape]>=0, 'Input error'
    return counts

def get_input_data() -> tuple:
    full=tuple(map(int,input('Data (c,r,I,J,L,O,S,T,Z) ?= ').split()))
    assert len(full)==9, 'Input error'
    return full[0],full[1],dict(zip('IJLOSTZ',full[2:]))

def generate_solution_space(input_data:tuple) -> list[list[int]]:
    board_columns,board_rows,tetris_counts=input_data

    total,mapped=0,0
    rev_count=[]
    for t,c in tetris_counts.items():
        if c:
            total+=c
            while mapped<total:
                rev_count.append(t)
                mapped+=1
    del t,c
    del total,mapped

    placements=[]
    for tetris in tetris_counts:
        if tetris_counts[tetris]:
            for rel_pos in REL_POS[tetris]:
                # rel_pos should be tuple[int,int] with len==4
                for r in range(board_rows):
                    for c in range(board_columns):
                        pos=[(r+d[0],c+d[1]) for d in rel_pos]
                        if all(list(map(lambda x: 0<=x[0]<board_rows and 0<=x[1]<board_columns, pos))):
                            # possible placement for a tetris
                            placements.append(tuple([tetris]+pos))
    del tetris,rel_pos,r,c
    del pos

    res=[]
    for placing in placements:
        # placing: (tetris,(),(),(),())
        tetris=placing[0]
        grid_ids=list(map(lambda x: x[0]*board_columns+x[1], placing[1:]))
        vector=[(1 if i in grid_ids else 0) for i in range(board_rows*board_columns)]
        for k in range(tetris_counts[tetris]):
            piece=[(1 if i==k+rev_count.index(tetris) else 0) for i in range(len(rev_count))]
            res.append(vector+piece)

    return res

def solve_exact_cover(matrix:DancingLink) -> list[list[int]]:
    final_selection=[]

    def recursive_selection(mat:DancingLink, selected_rows:list[int]):
        print(f'{selected_rows=}')

        nonlocal final_selection
        head=matrix.HEAD
        if head.right==head:
            final_selection=selected_rows
            return True

        first_column_head=head.right
        # checks if some column has no Node left
        c_head=first_column_head
        while c_head!=head:
            if c_head.down==c_head: return False
            c_head=c_head.right
        del c_head

        # row selection based on the first unsolved column, flag this column first
        mat.flag_column_head(first_column_head)
        # first Node for the chosen row
        chosen_row_head=first_column_head.down
        while chosen_row_head!=first_column_head:
            # stack
            current_selected_rows=selected_rows+[chosen_row_head.pos[0]]
            row_next=chosen_row_head.right
            while row_next!=chosen_row_head:
                # locate the columns to be flagged due to the latest row selection
                target_column_head=row_next.col
                mat.flag_column_head(target_column_head)
                row_next=row_next.right
            del row_next
            # recursion searching
            if recursive_selection(mat,current_selected_rows): return True
            else:
                # restore columns from current row selection, using reversed operations from above
                row_back=chosen_row_head.left
                while row_back!=chosen_row_head:
                    target_column_head=row_back.col
                    mat.unflag_column_head(target_column_head)
                    row_back=row_back.left
                del row_back,target_column_head
                current_selected_rows.pop()
                chosen_row_head=chosen_row_head.down
        # quits while-loop, indicating all trials on selecting rows from current first_column fails
        # don't forget to unflag the supposed first unsolved column
        mat.unflag_column_head(first_column_head)
        return False

    # base call
    recursive_selection(matrix,[])
    assert final_selection, 'No solution'
    return [matrix.source[i] for i in range(len(matrix.source)) if i+1 in final_selection]

def draw_board(solution:list[list[int]],grid_size:tuple[int,int]):
    global COLORS

    dirs={0:(0,1), 90: (-1,0), 180: (0,-1), 270: (1,0)}

    turtle.setup(800,600)
    turtle.title('Solution')
    turtle.pencolor('black')
    turtle.pensize(2)
    turtle.speed(10)
    turtle.hideturtle()

    turtle.clear()
    turtle.penup()
    turtle.home()

    def draw_tetris(v:list[int],size:tuple[int,int]):
        global COLORS
        nonlocal dirs

        # size=(col_count,row_count)
        grid_pos=[(i//size[0],i%size[0]) for i in range(len(v)) if v[i]==1]
        # grid_pos[0] surely has no block to its top/left
        start_pos=(-size[0]*UNIT/2+grid_pos[0][1]*UNIT, size[1]*UNIT/2-grid_pos[0][0]*UNIT)
        current_block=grid_pos[0]
        current_dir=0
        total_turning=0

        color=random.choice(COLORS)
        COLORS.remove(color)
        turtle.fillcolor(color)
        turtle.setpos(start_pos)
        turtle.setheading(current_dir)
        turtle.begin_fill()
        turtle.pendown()

        while abs(total_turning)!=360 or current_block!=grid_pos[0]:
            turtle.forward(UNIT)
            # turning
            delta=dirs[current_dir]
            # no block forward, then turn right
            if (current_block[0]+delta[0],current_block[1]+delta[1]) not in grid_pos:
                turtle.right(90)
                current_dir=(current_dir-90)%360
                total_turning-=90
            else:
                # forward block exists, first rebase current_block
                current_block=(current_block[0]+delta[0],current_block[1]+delta[1])
                # delta for the new left direction
                delta=dirs[(current_dir+90)%360]
                # the forward-left block exist, then turn left
                if (current_block[0]+delta[0],current_block[1]+delta[1]) in grid_pos:
                    turtle.left(90)
                    current_dir=(current_dir+90)%360
                    total_turning+=90
                    current_block=(current_block[0]+delta[0],current_block[1]+delta[1])
                # should continue going forward if forward-left doesn't exist

        turtle.penup()
        turtle.end_fill()

    solution.sort(reverse=True)
    num=len(solution)
    for vector in solution:
        draw_tetris(vector[:-num],grid_size)

    turtle.exitonclick()

def main():
    try:
        data=get_input_data()
        space=generate_solution_space(data)
        print(f'\nSOLUTION SPACE:')
        for i in range(len(space)): print(space[i])
        print()
        table=DancingLink.from_matrix(space)
        solution=solve_exact_cover(table)
        print(f'\nFINAL SOLUTION:')
        for i in range(len(solution)): print(solution[i])
        print()
        draw_board(solution,data[:2])
    except:
        from traceback import print_exc
        print_exc()

if __name__=='__main__':
    main()
