#this file auto-generates the TTH TTree header

function prefixed(pref::Symbol, t::Type, objs...)
    d = Dict()
    for o::Symbol in objs
        d[symbol(string(pref, "__", o))] = t
    end
    return d
end

function prefixed_dynlength(pref::Symbol, t::Type, objs...)
    d = Dict()
    merge!(d, prefixed(:n, Int32, pref))
    veclength = first(keys(d))
    for o::Symbol in objs
        d[symbol(string(pref, "__", o))] = (t, veclength)
    end
    return d
end

const type_map = {
    Float32 => "F",
    Float64 => "D",
    Int32 => "I",
}

const cpp_type_map = {
    Float32 => x->"float $x",
    Float64 => x->"double $x",
    Int32 => x->"int $x",
    Vector{Float32} => x->"float $x[N_MAX]",
    Vector{Int32} => x->"int $x[N_MAX]",
}

const DEF_VAL = {
    Float32 => x->"$x = DEF_VAL_FLOAT",
    Float64 => x->"$x = DEF_VAL_DOUBLE",
    Int32 => x->"$x = DEF_VAL_INT",
    Vector{Float32} => x->"SET_ZERO($x, N_MAX, DEF_VAL_FLOAT)",
    Vector{Int32} => x->"SET_ZERO($x, N_MAX, DEF_VAL_INT)",
}

branchtype(x) = x
branchtype(t::Tuple) = t[1]

function make_branch(out::IO, bn::Symbol, x::Tuple)
    bt = x[1]
    veclength = x[2]
    write(out, "tree->Branch(\"$bn\", ", "$bn, \"", bn, "[", veclength, "]/", type_map[eltype(bt)], "\");\n")
end

function make_branch(out::IO, bn::Symbol, bt::Any)
    write(out, "tree->Branch(\"$bn\", ", "&$bn, \"", bn ,"/", type_map[bt], "\");\n")
end


function make_branch_var(out::IO, bn::Symbol, bt::Type)
    write(out, cpp_type_map[bt](bn), ";\n")
end

ts() = write("\t");

function make_class(out::IO, name::Symbol, d::Dict)

    tree = sort(collect(d))
    write(out, "//Autogenerated\n")
    write(out, "#include <TTree.h>\n")
    write(out, "#define N_MAX 500\n")
    write(out, "#define DEF_VAL_FLOAT -9999.0f\n")
    write(out, "#define DEF_VAL_DOUBLE -9999.0d\n")
    write(out, "#define DEF_VAL_INT -9999\n")
    write(out, "#define FLOAT_EPS 0.0000001f\n")
    write(out, "#define DOUBLE_EPS 0.0000001d\n")
    write(out, "constexpr bool is_undef(int x) { return x==DEF_VAL_INT; };\n")
    write(out, "constexpr bool is_undef(float x) { return fabs(x-DEF_VAL_FLOAT) < FLOAT_EPS; };\n")
    write(out, "constexpr bool is_undef(double x) { return fabs(x-DEF_VAL_DOUBLE) < DOUBLE_EPS; };\n")
    write(out, "#define SET_ZERO(x,n,y) for(int i=0;i<n;i++) {x[i]=y;}\n")
    write(out, "class $name {\n")

    write("public:\n")
    ts();write("$name(TTree* _tree);\n")

    ts();write("TTree* tree;\n")
    for (k, v) in tree
        ts();make_branch_var(out, k, branchtype(v))
    end

    ts();write("void loop_initialize(void) {\n")
    for (k, v) in tree
        ts();ts();write(string(DEF_VAL[branchtype(v)](k), ";\n"))
    end
    ts();write("}\n")

    ts();write("void make_branches(void) {\n")

    #first make Int branches to get dynamic array counters
    for (k, v) in tree
        branchtype(v) != Int32 && continue
        ts();ts();make_branch(out, k, v)
    end
    for (k, v) in tree
        branchtype(v) == Int32 && continue
        ts();ts();make_branch(out, k, v)
    end
    ts();write("}\n")

    write(out, "};\n") #end class

end


#####
tree_structure = Dict()

particle_id = [:id]
fourmomentum = [:pt, :eta, :phi, :mass]
fourmomentum_cartesian = [:px, :py, :pz, :e]

#Leptons

merge!(tree_structure,
    prefixed_dynlength(:lep, Vector{Float32}, fourmomentum..., :riso, :dxy, :dz, :mva)
)

merge!(tree_structure,
    prefixed_dynlength(:lep, Vector{Int32}, particle_id..., :charge, :is_tight, :is_medium, :is_loose)
)

merge!(tree_structure,
    prefixed_dynlength(:gen_lep, Vector{Float32}, fourmomentum...)
)

merge!(tree_structure,
    prefixed_dynlength(:gen_lep, Vector{Int32}, particle_id...)
)

#Jets
merge!(tree_structure,
    prefixed_dynlength(:jet, Vector{Float32}, fourmomentum..., :bd_csv)
)

merge!(tree_structure,
    prefixed_dynlength(:jet, Vector{Int32}, particle_id...)
)

merge!(tree_structure,
    prefixed_dynlength(:gen_jet, Vector{Float32}, fourmomentum...)
)

merge!(tree_structure,
    prefixed_dynlength(:gen_jet, Vector{Int32}, particle_id...)
)

#MET
merge!(tree_structure,
    prefixed(:met, Float32, :pt, :phi, :pt__en_up, :pt__en_down)
)

merge!(tree_structure,
    prefixed(:gen_met, Float32, :pt, :phi)
)

#Weights
merge!(tree_structure,
    prefixed(:weight, Float32, :pu, :pu__up, :pu_down, :trigger, :trigger_up, :trigger_down)
)

#Per-event info
merge!(tree_structure,
    prefixed(:event, Int32, :run, :lumi, :id, :json)
)

merge!(tree_structure,
    prefixed(:debug, Float64, :time1r, :time1c)
)

#pv - primary vertices
merge!(tree_structure,
    prefixed(:n, Int32, :pv)
)
merge!(tree_structure,
    prefixed_dynlength(:pvi, Vector{Float32}, :ntrue, :n0)
)
merge!(tree_structure,
    prefixed_dynlength(:pvi, Vector{Int32}, :bx)
)
#####

make_class(STDOUT, :TTHTree, tree_structure)