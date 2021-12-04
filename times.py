
#time should be stored as 0 (12 AM) - 23 (11 PM)
# ex: 0-4

#https://www.w3schools.com/python/python_classes.asp

class Frames: 
    def __init__(self, min, max): 
        self.min = min 
        self.max = max     
    def setMin(self, min):
        self.min = min
    def setMax(self, max): 
        self.max = max 
    
    @Override
    public boolean equals(Object obj) {
        return (((Frames) obj).getMin() == (getMin())&& ((Frames)obj).getMax()==(getMax()));
    }

    @Override
    public int compareTo(Object o) {

        Frames i = (Frames) o;
        return getMin() - (i.getMin());
    }
    public boolean intersect (Frames one, Frames two)
    {
        if(one.getMin()<=two.getMax() && one.getMin()>=two.getMin())
        {
            return true;
        }
        else if (one.getMax()>=two.getMin() && one.getMax()<=two.getMax())
        {
            return true;
        }
        return false;

    }
    public int getPeriod()
    {
        return maximum-minimum;
    }

}

