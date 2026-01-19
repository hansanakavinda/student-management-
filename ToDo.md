1. done

2. done 

3. done

4. student details and exam details table related issues
     4.1 there is a small UI issue in the system when the one students name is longer than the given lenght of the student view table it expands teh column and it misses consistency. because all the other column move away while the table header stay in the same place. 

     there are two solutions for this.
          1. we can trucate the student name if it tries to exceed the column lenght.
          2. or we could make teh table adjust its column lenght based on the student name. while maintaining consistency with other names and columns

          there are two tables affected by this student profile view and student exam results view.

     I would like if it is possible to adjust the lenght of the columns to view truncated values if possible. from the solutions and suggest implement the easiest and most effective solution.

     4.2 currently the student profile view table use paginatoin to handle large student count. I want similar mechanisam implemented in exam results view. so it does not load all the records at once which could take more time or freeze UI when the system get loaded with real data. 

5. student profile exam marks view.
    add a button to download students marks history into a pdf. which should also be saved to the folder with student name and id.

6. input validation