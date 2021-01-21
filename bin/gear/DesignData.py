import math;
class DesignData():
    MODULES=[1,1.125,1.25,1.375,1.5,1.75,2,2.25,2.5,2.75,3,3.5,4,4.5,5,
            5.5,6,6.5,7,8,9,10,11,12,14,16,18,20,22,25,28,32,36,40,45,50];
    def getGrade(grade):
        if grade=="1":
            constant1=0.8;
            constant2=0.06;
        if grade=="2":
            constant1=1.25;
            constant2=0.10;
        if grade=="3":
            constant1=2.0;
            constant2=0.16;
        if grade=="4":
            constant1=3.2;
            constant2=0.25;
        if grade=="5":
            constant1=5.0;
            constant2=0.4;
        if grade=="6":
            constant1=8.0;
            constant2=0.63;
        if grade=="7":
            constant1=11.0;
            constant2=0.9;
        if grade=="8":
            constant1=16.0;
            constant2=1.25;
        if grade=="9":
            constant1=22.0;
            constant2=1.80;
        if grade=="10":
            constant1=32.0;
            constant2=2.5;
        if grade=="11":
            constant1=45.0;
            constant2=3.55;
        if grade=="12":
            constant1=63.0;
            constant2=5.0;
        return constant1, constant2;
    def evalGearing(gearing,gearTeeth,pinionTeeth):
        if gearing=="Internal gearing":
            return ((2*gearTeeth/pinionTeeth)/((gearTeeth/pinionTeeth)-1)), "Internal gearing";
        if gearing=="External gearing":
            return ((2*gearTeeth/pinionTeeth)/((gearTeeth/pinionTeeth)+1)), "External gearing";
    def evalProfile(profile):
        if profile=="14.5 degree full depth involute tooth":
            return {
                    "lewisFactor":
                                    {
                                        "pinion":
                                                "0.124-(0.684/pinionTeeth)",
                                        "gear":
                                                "0.124-(0.684/gearTeeth)"
                                    },
                    "pressureAngle":
                                    "14.5",
                    "deformationFactor":
                                        "0.107/((1/self.pinionElasticity)+(1/self.gearElasticity))",
                    "profile":
                              "Full depth involute tooth"
                    }
        if profile=="20 degree full depth involute tooth":
            return {
                    "lewisFactor":
                                    {
                                        "pinion":
                                                "0.154-(0.912/pinionTeeth)",
                                        "gear":
                                                "0.154-(0.912/gearTeeth)"
                                    },
                    "pressureAngle":
                                    "20",
                    "deformationFactor":
                                        "0.111/((1/self.pinionElasticity)+(1/self.gearElasticity))",
                    "profile":
                              "Full depth involute tooth"
                    }
        if profile=="20 degree stub involute tooth":
            return {
                    "lewisFactor":
                                    {
                                        "pinion":
                                                "0.175-(0.95/pinionTeeth)",
                                        "gear":
                                                "0.175-(0.95/gearTeeth)"
                                    },
                    "pressureAngle":
                                    "20",
                    "deformationFactor":
                                        "0.115/((1/self.pinionElasticity)+(1/self.gearElasticity))",
                    "profile":
                              "Stub involute tooth"
                    }
    def evalTolerance(module,teeth,grade):
        constant1, constant2=DesignData.getGrade(grade);
        phi=module+0.25*math.sqrt(module*teeth);
        error=constant1+constant2*phi;
        return (error/1000);
