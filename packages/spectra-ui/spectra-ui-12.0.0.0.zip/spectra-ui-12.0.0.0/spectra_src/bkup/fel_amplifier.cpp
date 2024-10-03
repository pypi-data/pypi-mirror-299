#include "fel_amplifier.h"
#include "trajectory.h"
#include "flux_density.h"
#include "common.h"
#include "particle_generator.h"

// files for debugging
string FELTempProfile;
string FELSpecProfile;
string FELCurrProfileDebug;
string FELBunchFactorDebug;
string ParticleDist6D;
string FELTrajectory;
int TargetParticle = 0;

FELAmplifier::FELAmplifier(
    SpectraSolver& spsolver, Trajectory *trajectory, FilterOperation *filter, int fellayer)
    : CoherentRadiationBase(spsolver, trajectory, filter)
{
#ifdef _DEBUG
    FELTempProfile = "..\\debug\\fel_temporal.dat";
    FELSpecProfile = "..\\debug\\fel_spectrum.dat";
    FELCurrProfileDebug = "..\\debug\\fel_current.dat";
    FELBunchFactorDebug = "..\\debug\\fel_bfactor.dat";
//    ParticleDist6D = "..\\debug\\particles6d.dat";
//    FELTrajectory = "..\\debug\\fel_trajectory.dat";
#endif

//--------->>>>>>>>>>>>
//ParticleDist6D = "..\\debug\\particles6d.dat";
    FELTempProfile = "..\\debug\\fel_temporal.dat";


    m_fellayer = fellayer;
    InitFluxDensity(m_trajectory, filter);

    vector<vector<double>> betaarr(2);
    vector<double> rz;
    m_trajectory->GetTrajectory(m_zorbit, nullptr, &m_kick, nullptr, &rz);
    m_trajectory->TransferTwissParamaters(nullptr, nullptr, &betaarr);
    m_trajectory->GetZsection(m_secidx);
    m_nsections = (int)m_secidx[1].size();

    for(int nsec = 0; nsec < m_nsections-1; nsec++){
        m_Zi.push_back((m_zorbit[m_secidx[1][nsec+1]]+m_zorbit[m_secidx[1][nsec]])*0.5);
    }
    m_Zi.push_back(m_conf[slit_dist_]);

    Spline betaspl[2];
    m_tstep.resize(m_nsections);
    m_bmsize.resize(2);
    for(int j = 0; j < 2; j++){
        m_bmsize[j].resize(m_nsections);
        betaspl[j].SetSpline((int)m_zorbit.size(), &m_zorbit, &betaarr[j]);
    }
    m_bmmax[0] = m_bmmax[1] = 0;
    m_t0 = -(m_zorbit[0]+m_gamma2*rz[0])/m_time2tau; // time delay at the entrance    
    for(int nsec = 0; nsec < m_nsections; nsec++){
        m_tstep[nsec] = -(m_zorbit[m_secidx[1][nsec]]+m_gamma2*rz[m_secidx[1][nsec]])/m_time2tau;
        // time delay at the end of each section
        double zmid = (m_zorbit[m_secidx[0][nsec]]+m_zorbit[m_secidx[1][nsec]])*0.5;
        for(int j = 0; j < 2; j++){
            m_bmsize[j][nsec] = sqrt(betaspl[j].GetValue(zmid)*m_emitt[j]);
            // beam size at the middle of each section
            m_bmmax[j] = max(m_bmmax[j], m_bmsize[j][nsec]);
        }
    }

    double lregmin = minmax(m_lregsec, false);
    for(int j = 0; j < 2; j++){
        m_dXY[j] = m_dxy[j] = m_bmmax[j]/2; // maximum grid; beam size/2
        m_dxy[j] = min(m_dxy[j], lregmin*wave_length(m_ep.back())/4/(2*m_bmmax[j]));
        double Zobs = max(lregmin, m_Zi.back()-m_zorbit.back());
        m_dXY[j] = min(m_dXY[j], Zobs*wave_length(m_ep.back())/4/m_xyfar[j]);
    }
    m_ws = nullptr;
    m_spfft = nullptr;
    ArrangeObservation(m_bmmax, m_dxy);

    m_bunchf.resize(m_nsections);
    for(int nsec = 0; nsec < m_nsections; nsec++){
        m_bunchf[nsec].resize(2);
        for(int j = 0; j < 2; j++){
            m_bunchf[nsec][j].resize(m_nfd, 0);
        }
    }

    // define the FFT-related parameters
    for(int j = 0; j < 2; j++){
        // compute at the largest off-axis position
        m_XYZ[j] = m_xygrid[j].back();
    }

    // longitudinal position near to the exit
    m_XYZ[2] = m_zorbit.back()+minmax(m_lregsec, false);
    f_AllocateElectricField(false, true, true);
    if(!f_SetupFTConfig()){
        throw runtime_error("Not enough memory available for FFT.");
        return;
    }

    m_dt = m_dtau/m_time2tau;
    if(m_fft_nskip > 1){
        // shrink time interval because energy pitch is expanded
        m_dt /= m_fft_nskip;
    }
    m_tgrid.resize(m_nfft+1);
    for(int n = 0; n <= (int)m_nfft; n++){
        m_tgrid[n] = m_dt*(n-(int)m_nfft/2);
    }

    ArrangeEtGrid();

    //--------->>>>>>
    double pkpower = 1e-9;
    double epcenter = 4.49637;
    double plen = 4e-14;
    double srcsize = 5e-3;
    double zwaist = 0;
    double torg = 0;
    m_seed = new SeedLight(pkpower, epcenter, plen, srcsize, zwaist, torg);

    //------>>>>>>>
    int Nparticles = 10000;
    m_reference.Clear();
    if(!f_SetEtSpace(Nparticles)){
        throw runtime_error("Too few macroparticles.");
    }

#ifdef _DEBUG
    if(!FELTrajectory.empty()){
        ofstream debug_out(FELTrajectory);
        vector<string> titles {"z", "xref", "x", "yref", "y", "x'ref", "x'", "y'ref", "y'", "tref", "t", "DEref", "DE/E"};
        vector<double> items(13);
        PrintDebugItems(debug_out, titles);
        items[0] = m_zorbit[0];
        for(int j = 0; j < 2; j++){
            items[2*j+1] = m_reference._xy[j];
            items[2*j+2] = m_particles[TargetParticle]._xy[j];
            items[2*j+5] = m_reference._qxy[j];
            items[2*j+6] = m_particles[TargetParticle]._qxy[j];
            items[2*j+9] = m_reference._tE[j];
            items[2*j+10] = m_particles[TargetParticle]._tE[j];
        }
        PrintDebugItems(debug_out, items);
        debug_out.close();
    }
#endif
}

FELAmplifier::~FELAmplifier()
{
    delete m_spfft;
    if(m_seed != nullptr){
        delete m_seed;
    }
    f_FreeWS();
}

void FELAmplifier::f_FreeWS()
{
    for(int n = 0; n < m_ngfft[0]; n++){
        delete[] m_ws[n];
    }
    delete[] m_ws;
}


void FELAmplifier::AdvanceSection(int tgtsec)
{
    if(tgtsec == m_nsections){
        ArrangeObservation(m_xyfar, m_dXY);
        ArrangeEtGrid();
        f_GetComplexAmpAt(m_nsections-1, nullptr, m_istime);
    }
    else{
        f_GetComplexAmpAt(tgtsec-1); // compute the E-field at the entrance (exit of the previous section)
        f_GetBunchFactor(tgtsec); // compute the bunch factor at the entrance 
        f_AdvanceParticles(tgtsec); // advance particles to the exit
    }
}

void FELAmplifier::GetValues(double *xyobsin, vector<double> *values)
{
    double xyobs[2];
    for(int j = 0; j < 2; j++){
        xyobs[j] = xyobsin == nullptr ? m_center[j] : xyobsin[j];
    }

    if(xyobsin == nullptr){
        // directly evaluate at the observation position
        f_GetComplexAmpAt(m_nsections-1, xyobs, m_istime);
    }
    f_GetValues(xyobsin, *values, m_istime);
}

int FELAmplifier::GetTotalSteps()
{
    int steps = 0;
    for(int n = 0; n < m_nsections; n++){
        steps += f_GetSteps(n);
    }
    steps += m_nsections+2;
    return steps;
}

void FELAmplifier::ArrangeObservation(double Dxy[], double dxy[])
{
    if(m_ws != nullptr){
        f_FreeWS();
    }
    if(m_spfft != nullptr){
        delete m_spfft;
    }

    for(int j = 0; j < 2; j++){
        m_ngfft[j] = (int)floor(0.5+Dxy[j]/dxy[j]*(2*m_gaussian_limit)*1.5);
        m_ngfft[j] = fft_number(m_ngfft[j], 1);
        m_nghalf[j] = m_ngfft[j]/2-1;
        m_xygrid[j].resize(2*m_nghalf[j]+1);
        for(int n = -m_nghalf[j]; n <= m_nghalf[j]; n++){
            m_xygrid[j][n+m_nghalf[j]] = n*dxy[j];
        }
    }
    int ntot = (2*m_nghalf[0]+1)*(2*m_nghalf[1]+1);
    for(int j = 0; j < 4; j++){
        m_FxyGrid[j].resize(ntot);
        m_SxyGrid[j].resize(ntot);
        for(int n = 0; n < ntot; n++){
            m_FxyGrid[j][n].resize(m_nfd);
            m_SxyGrid[j][n].resize(m_nfd);
        }
    }

    m_ws = new double *[m_ngfft[0]];
    for(int n = 0; n < m_ngfft[0]; n++){
        m_ws[n] = new double[2*m_ngfft[1]];
    }
    m_spfft = new FastFourierTransform(2, m_ngfft[0], m_ngfft[1]);
}

void FELAmplifier::ArrangeEtGrid()
{
    m_EtGrid.resize(2*m_nghalf[0]+1);
    for(int nx = 0; nx <= 2*m_nghalf[0]; nx++){
        m_EtGrid[nx].resize(2*m_nghalf[1]+1);
        for(int ny = 0; ny <= 2*m_nghalf[1]; ny++){
            m_EtGrid[nx][ny].resize(2);
            for(int j = 0; j < 2; j++){
                m_EtGrid[nx][ny][j].resize(m_nfft+1);
            }
        }
    }
}

void FELAmplifier::GetBunchInf(vector<double> &zstep, vector<double> &energy,
    vector<vector<vector<double>>> &bunchf, vector<double> &currt, vector<vector<double>> &currI)
{
    zstep.resize(m_nsections);
    for(int n = 0; n < m_nsections; n++){
        zstep[n] = m_zorbit[m_secidx[0][n]];
    }
    energy = m_ep;
    bunchf = m_bunchf;
    currt = m_currt;
    currI = m_currI;
}

// private functions
int FELAmplifier::f_GetSteps(int tgtsec)
{
    int steps = (tgtsec+1)+2; // f_GetComplexAmpAt
    steps++; // f_GetBunchFactor
    steps += (int)floor(m_Nparticles/STEPSPARTICLES); // f_AdvanceParticles
    return steps;
}

void FELAmplifier::f_GetValues(double *xyobs, vector<double> &values, bool istime)
{
    double dindex[2];
    vector<int> nxy[2];
    if(xyobs == nullptr){
        for(int j = 0; j < 2; j++){
            nxy[j] = vector<int> {m_nghalf[j]};
        }
    }
    else{
        int il[3];
        for(int j = 0; j < 2; j++){
            il[j] = get_index4lagrange(xyobs[j], m_xygrid[j], 2*m_nghalf[j]+1);
            dindex[j] = xyobs[j]/m_dxy[j]+m_nghalf[j]-(il[j]-1);
        }
        for(int j = 0; j < 2; j++){
            nxy[j] = vector<int>{il[j]-1, il[j], il[j]+1};
        }
    }

    int mesh = istime ? (int)m_tarray.size() : m_nfd;
    int jm = istime ? 2 : 4;
    if(m_wsef.size() == 0){
        m_wsef.resize(jm*mesh);
        for(int n = 0; n < jm*mesh; n++){
            m_wsef[n].resize(nxy[0].size());
            for(int ix = 0; ix < nxy[0].size(); ix++){
                m_wsef[n][ix].resize(nxy[1].size());
            }
        }
    }

    if(istime){
        f_GetValuesTimeAt(nxy[0], nxy[1]);
    }
    else{
        int nflux = m_isfluxs0?1:4;
        if(values.size() < m_nfd*nflux){
            values.resize(m_nfd*nflux);
        }
        f_GetValuesFluxAt(nxy[0], nxy[1]);
    }

    double vtmp[4], fx[2], fy[2];
    vector<double> fxy(4);
    for(int n = 0; n < mesh; n++){
        for(int j = 0; j < jm; j++){
            if(xyobs == nullptr){
                vtmp[j] = m_wsef[n+j*mesh][0][0];
            }
            else{
                vtmp[j] = lagrange2d(m_wsef[n+j*mesh], dindex);
            }
            if(istime){
                values[n+j*mesh] = vtmp[j];
            }
        }
        if(!istime){
            if(m_isfluxamp){
                for(int j = 0; j < 4; j++){
                    values[n+j*m_nfd] = vtmp[j];
                }
            }
            else if(m_isfluxs0){
                values[n] = hypotsq(vtmp[0], vtmp[1])+hypotsq(vtmp[2], vtmp[3]);
            }
            else{
                for(int j = 0; j < 2; j++){
                    fx[j] = vtmp[j];
                    fy[j] = vtmp[j+2];
                }
                stokes(fx, fy, &fxy);
                for(int j = 0; j < 4; j++){
                    values[n+j*m_nfd] = fxy[j];
                }
            }
        }
    }
}

void FELAmplifier::f_GetValuesTimeAt(vector<int> &nx, vector<int> &ny)
{
    int tmesh = (int)m_tarray.size();
    double coef = GetTempCoef(true);
    for(int ix = 0; ix < nx.size(); ix++){
        for(int iy = 0; iy < ny.size(); iy++){
            for(int j = 0; j < 2; j++){
                m_EtSpline[j].SetSpline(m_nfft+1, &m_tgrid,
                    &m_EtGrid[nx[ix]][ny[iy]][j]);
            }
            for(int n = 0; n < tmesh; n++){
                for(int j = 0; j < 2; j++){
                    m_wsef[n+j*tmesh][ix][iy] = m_EtSpline[j].GetValue(m_tarray[n])/coef;
                }
            }
        }
    }
}

void FELAmplifier::f_GetValuesFluxAt(vector<int> &nx, vector<int> &ny)
{
    for(int ix = 0; ix < nx.size(); ix++){
        for(int iy = 0; iy < ny.size(); iy++){
            int nxyorg = nx[ix]+ny[iy]*(2*m_nghalf[0]+1);
            for(int n = 0; n < m_nfd; n++){
                for(int j = 0; j < 4; j++){
                    m_wsef[n+j*m_nfd][ix][iy] = m_SxyGrid[j][nxyorg][n];
                }
            }
        }
    }
}

void FELAmplifier::f_AdvanceParticles(int tgtsection)
{
    vector<vector<double>> *Exy;
    int nidx[2];

    double tdelay = tgtsection == 0 ? m_t0-m_tstep[0] : m_tstep[tgtsection-1]-m_tstep[tgtsection];
    // time delay of a reference electron in this section with respect to radiation 

#ifdef _DEBUG
    vector<vector<double>> items;
    vector<double> item(13);
#endif

    for(int m = 0; m < m_Nparticles; m++){
        for(int j = 0; j < 2; j++){
            nidx[j] = (int)floor((m_particles[m]._xy[j]-m_xygrid[j][0])/m_dxy[j]+0.5);
        }
        if(nidx[0] >= 0 && nidx[0] < m_xygrid[0].size()
            && nidx[1] >= 0 && nidx[1] < m_xygrid[0].size()){
            Exy = &m_EtGrid[nidx[0]][nidx[1]];
        }
        else{
            Exy = nullptr;
        }
        for(int nz = 2*m_secidx[0][tgtsection]+2; nz <= 2*m_secidx[1][tgtsection]; nz += 2){
            m_trajectory->AdvancePhaseSpace(nz-2, m_tgrid, Exy, m_particles[m]);
#ifdef _DEBUG
            if(!FELTrajectory.empty() && m == TargetParticle){
                m_trajectory->AdvancePhaseSpace(nz-2, m_tgrid, Exy, m_reference);
                // m_reference: reference particle for debugging
                item[0] = m_zorbit[nz/2];
                for(int j = 0; j < 2; j++){
                    item[2*j+1] = m_reference._xy[j];
                    item[2*j+2] = m_particles[TargetParticle]._xy[j];
                    item[2*j+5] = m_reference._qxy[j];
                    item[2*j+6] = m_particles[TargetParticle]._qxy[j];
                    item[2*j+9] = m_reference._tE[j];
                    item[2*j+10] = m_particles[TargetParticle]._tE[j];
                }
                items.push_back(item);
            }
#endif
        }
        // adjust time
        m_particles[m]._tE[0] -= tdelay;

#ifdef _DEBUG
        if(!FELTrajectory.empty() && m == TargetParticle){
            m_reference._tE[0] -= tdelay;
        }
#endif
        if((m+1)%STEPSPARTICLES == 0){
            m_calcstatus->AdvanceStep(m_fellayer);
        }
    }
    m_calcstatus->AdvanceStep(m_fellayer);

#ifdef _DEBUG
    if(!FELTrajectory.empty()){
        ofstream debug_out(FELTrajectory, ios_base::app);
        for(int n = 0; n < items.size(); n++){
            PrintDebugItems(debug_out, items[n]);
        }
        debug_out.close();
    }
#endif

//----->>>>
//#ifdef _DEBUG
    if(!ParticleDist6D.empty()){
        ofstream debug_out(ParticleDist6D);
        vector<string> titles {"x", "y", "x'", "y'", "t", "DE/E"};
        vector<double> items(6);
        PrintDebugItems(debug_out, titles);
        for(int m = 0; m < m_Nparticles; m++){
            for(int j = 0; j < 2; j++){
                items[j] = m_particles[m]._xy[j];
                items[j+2] = m_particles[m]._qxy[j];
                items[j+4] = m_particles[m]._tE[j];
            }
            items[4] *= 1e15;
            PrintDebugItems(debug_out, items);
        }
        debug_out.close();
    }
//#endif
}

bool FELAmplifier::f_SetEtSpace(int Nmax)
{
    double glimt = 4, glime = 3;
    double sigtE[2], dtE[2];
    int ntE[2], htE[2], m[2];
    sigtE[0] = m_acc[bunchlength_]*0.001/CC;
    sigtE[1] = m_acc[espread_];
    dtE[0] = m_dt;

    htE[0] = (int)floor(glimt*sigtE[0]/dtE[0]);
    ntE[0] = 2*htE[0]+1;

    m_currt.resize(ntE[0]);
    m_currI.resize(m_nsections);
    for(int nsec = 0; nsec < m_nsections; nsec++){
        m_currI[nsec].resize(ntE[0]);
    }
    for(m[0] = -htE[0]; m[0] <= htE[0]; m[0]++){
        m_currt[m[0]+htE[0]] = m_dt*m[0]*1e15;
    }

    htE[1] = Nmax/(htE[0]*2)/2;
    //-------->>>>>>>
    //if(htE[1] < 5){
    if(htE[1] < 3){
        return false;
    }
    ntE[1] = 2*htE[1]+1;
    dtE[1] = glime*sigtE[1]/htE[1];
    m_Nparticles = ntE[0]*ntE[1]-1;

    ParticleGenerator partgen(*this, m_trajectory);
    partgen.Init();
    partgen.Generate(m_particles, m_Nparticles/2);
    m_charge.resize(m_Nparticles);

    RandomUtility rand;
    rand.Init(1);

    vector<double> shotnoize(ntE[0], 0);
    int np = 0;
    for(m[1] = -htE[1]; m[1] <= htE[1]; m[1]++){
        for(m[0] = -htE[0]; m[0] <= htE[0]; m[0]++){
            for(int j = 0; j < 2; j++){
                m_particles[np]._tE[j] = m[j]*dtE[j];
            }
            if(m[1] == -htE[1]){
                double electrons = f_ElectronNumber(m_particles[np]._tE[0]);
                if(electrons > 0){
                    shotnoize[m[0]+htE[0]] = rand.Gauss(true)/sqrt(electrons);
                }
                //---------->>>>>>>
                shotnoize[m[0]+htE[0]]=0;

            }
            m_charge[np] = m_Nparticles*f_GetCharge(m_particles[np], dtE)*(1+shotnoize[m[0]+htE[0]]);
            np++;
            if(np == m_Nparticles){
                break;
            }
        }
        if(np == m_Nparticles){
            break;
        }
    }

    double tcharge = vectorsum(m_charge, m_Nparticles);
    m_charge *= m_Nparticles/tcharge;
    return true;
}

double FELAmplifier::f_GetCharge(Particle &particle, double dtE[])
{
    double sigtE[2];
    sigtE[0] = m_acc[bunchlength_]*0.001/CC;
    sigtE[1] = m_acc[espread_];

    double tex = hypotsq(particle._tE[0]/sigtE[0], particle._tE[1]/sigtE[1])*0.5;
    if(tex > MAXIMUM_EXPONENT){
        return 0;
    }
    return exp(-tex)/PI2/sigtE[0]/sigtE[1]*dtE[0]*dtE[1];
}

double FELAmplifier::f_ElectronNumber(double t)
{
    double sigt = m_acc[bunchlength_]*0.001/CC;
    double tex = t/sigt;
    tex *= 0.5*tex;
    if(tex > MAXIMUM_EXPONENT){
        return 0;
    }
    return m_bunchelectrons*m_dt/SQRTPI2/sigt*exp(-tex);
}

void FELAmplifier::f_SetTime()
{

    double sigt = m_acc[bunchlength_]*0.001/CC;
    double ti, tex;
    int Ni, np = 0;

    int nsig = (int)floor(6*sigt/m_dt+0.5); // at least 1 particle within +- 3sigma
    for(int n = -nsig; n <= nsig; n++){
        int idx = fft_index(n, m_nfft, -1);
        if(idx >= 0 && idx < (int)m_nfft){
            m_particles[np++]._tE[0] = n*m_dt;
        }
    }

    int nrep = 1;
    do{
        int Np = m_Nparticles-np;
        int n = 0;
        do{
            ti = n*m_dt;
            tex = ti*ti/sigt/sigt*0.5;
            if(tex > MAXIMUM_EXPONENT){
                Ni = 0;
            }
            else{
                Ni = (int)floor(Np/SQRTPI2/sigt*m_dt*exp(-tex)+nrep/4.0);
            }
            // adjut the threshold to judge if Ni >= 1
            for(int ni = 0; ni < Ni; ni++){
                m_particles[np++]._tE[0] = ti;
                if(np >= m_Nparticles){
                    return;
                }
            }
            if(n == 0){
                n++;
            }
            else if(n > 0){
                n = -n;
            }
            else{
                n = -n+1;
            }
        } while(n != -(int)m_nfft/2);
        nrep++;
    } while(np < m_Nparticles);
}

void FELAmplifier::f_AdjustCharge()
{
    for(int n = 0; n < 2*(int)m_nfft; n++){
        m_EwFFT[0][n] = 0;
    }

    vector<int> ibin(m_Nparticles);
    for(int n = 0; n < m_Nparticles; n++){
        int nr = (int)floor(0.5+m_particles[n]._tE[0]/m_dt);
        ibin[n] = fft_index(nr, m_nfft, -1);
        if(ibin[n] >= 0 && ibin[n] < (int)m_nfft){
            m_EwFFT[0][ibin[n]] += 1.0/m_Nparticles;
            m_particles[n]._tE[0] = nr*m_dt;
        }
    }

    double Ni, ti;
    double sigt = m_acc[bunchlength_]*0.001/CC;
    vector<double> weight(m_nfft, 1.0);
    for(int n = 0; n < (int)m_nfft; n++){
        if(m_EwFFT[0][n] == 0){
            continue;
        }
        int idx = fft_index(n, m_nfft, 1);
        ti = idx*m_dt/sigt;
        ti *= ti*0.5;
        if(ti < MAXIMUM_EXPONENT){
            Ni = 1/SQRTPI2/sigt*m_dt*exp(-ti);
        }
        else{
            Ni = 0;
        }
        weight[n] = Ni/m_EwFFT[0][n];
    }

    for(int n = 0; n < m_Nparticles; n++){
        if(ibin[n] >= 0 && ibin[n] < (int)m_nfft){
            m_charge[n] = weight[ibin[n]];
        }
    }
}

void FELAmplifier::f_GetBunchFactor(int tgtsection)
    // compute the current bunch factor and save in m_bunchf[tgtsection]
{
    for(int n = 0; n < 2*(int)m_nfft; n++){
        m_EwFFT[0][n] = 0;
    }

    int nr[2];
    for(int n = 0; n < m_Nparticles; n++){
        double dnt = m_particles[n]._tE[0]/m_dt;
        nr[0] = (int)floor(dnt);
        nr[1] = nr[0]+1;
        for(int i = 0; i < 2; i++){
            int idx = fft_index(nr[i], m_nfft, -1);
            if(idx >= 0 && idx < (int)m_nfft){
                m_EwFFT[0][idx] += fabs(nr[1-i]-dnt)*m_charge[n]/m_Nparticles;
            }
        }
    }

    int nh = (m_currt.size()-1)/2;
    for(int n = -nh; n <= nh; n++){
        int idx = fft_index(n, m_nfft, -1);
        m_currI[tgtsection][n+nh] = m_EwFFT[0][idx]*m_bunchelectrons*QE/m_dt;
    }

#ifdef _DEBUG
    if(!FELCurrProfileDebug.empty()){
        ofstream debug_out(FELCurrProfileDebug);
        vector<string> titles{"time(fs)", "I(A)"};
        vector<double> items(2);
        PrintDebugItems(debug_out, titles);
        for(int n = 0; n < m_currt.size(); n++){
            items[0] = m_currt[n];
            items[1] = m_currI[tgtsection][n];
            PrintDebugItems(debug_out, items);
        }
        debug_out.close();
    }
#endif

    m_fft->DoRealFFT(m_EwFFT[0]);
    for(int ne = 0; ne < m_nfd; ne++){
        if(ne == 0){
            m_bunchf[tgtsection][0][ne] = m_EwFFT[0][0];
            m_bunchf[tgtsection][1][ne] = 0;
        }
        for(int j = 0; j < 2; j++){
            m_bunchf[tgtsection][j][ne] = m_EwFFT[0][2*ne+j];
        }
    }
    m_calcstatus->AdvanceStep(m_fellayer);

#ifdef _DEBUG
    if(!FELBunchFactorDebug.empty()){
        ofstream debug_out(FELBunchFactorDebug);
        vector<string> titles{"ep(eV)", "Bre", "Bim"};
        vector<double> items(3);
        PrintDebugItems(debug_out, titles);
        for(int ne = 0; ne < m_nfd; ne++){
            items[0] = m_ep[ne];
            for(int j = 0; j < 2; j++){
                items[j+1] = m_bunchf[tgtsection][j][ne];
            }
            PrintDebugItems(debug_out, items);
        }
        debug_out.close();
    }
#endif
}

void FELAmplifier::f_GetComplexAmpAt(int tgtindex, double *xyobs, bool istime)
{
    double xy[2], ExyS[4];
    double coef = GetTempCoef(true);
    double scoef = m_gamma2/PI*m_time2tau/coef;
    // m_gamma2/PI : Dw = Fw * gamma^2/Pi *(-i)
    // m_time2tau : dtau = 2*gamma^2*c dt

    for(int nx = 0; nx <= 2*m_nghalf[0]; nx++){
        xy[0] = m_xygrid[0][nx];
        for(int ny = 0; ny <= 2*m_nghalf[1]; ny++){
            xy[1] = m_xygrid[1][ny];
            int nxy = nx+ny*(2*m_nghalf[0]+1);
            for(int j = 0; j < 4; j++){
                fill(m_SxyGrid[j][nxy].begin(), m_SxyGrid[j][nxy].end(), 0.0);
            }
            for(int j = 0; j < 2 && xyobs != nullptr; j++){
                xy[j] += xyobs[j];
            }
            if(m_seed != nullptr){
                for(int n = 0; n < m_nfd; n++){
                    if(tgtindex < 0){
                        m_seed->GetAmplitudeS(m_ep[n], m_t0, m_zorbit[0], xy, ExyS);
                    }
                    else if(tgtindex == m_nsections-1){
                        m_seed->GetAmplitudeS(m_ep[n], m_tstep[tgtindex], m_Zi[m_nsections-1], xy, ExyS);
                    }
                    else{
                        m_seed->GetAmplitudeS(m_ep[n],
                            m_tstep[tgtindex], m_zorbit[m_secidx[1][tgtindex]], xy, ExyS);
                    }
                    // *(-i); swap real/imaginary & negate imaginary
                    swap(ExyS[0], ExyS[1]); ExyS[1] *= -1;
                    swap(ExyS[2], ExyS[3]); ExyS[3] *= -1;
                    for(int j = 0; j < 4; j++){
                        // convert seed field to "Dw"
                        m_SxyGrid[j][nxy][n] = ExyS[j]*scoef;
                    }
                }
            }
        }
    }
    m_calcstatus->AdvanceStep(m_fellayer);

    if(tgtindex >= 0){
        f_GetComplexAmpMB(tgtindex, xyobs);
    }

#ifdef _DEBUG
    if(!FELSpecProfile.empty() && tgtindex >= 0){
        ofstream debug_out(FELSpecProfile);
        vector<int> eppick;
        
        int ned = 20;
        double eplim = 10;
        for(int n = 1; n < m_nfd; n+=ned){
            eppick.push_back(n);
            if(m_ep[n] > eplim){
                break;
            }
        }

        vector<string> titles(2+2*eppick.size());
        vector<double> items(2+2*eppick.size());
        titles[0] = "x(mm)";
        titles[1] = "y(mm)";
        for(int n = 0; n < eppick.size(); n++){
            titles[2*n+2] = "Ex.re"+to_string(m_ep[eppick[n]]);
            titles[2*n+3] = "Ex.im"+to_string(m_ep[eppick[n]]);
        }
        PrintDebugItems(debug_out, titles);
        int ny = m_nghalf[1];
        for(int nx = 0; nx <= 2*m_nghalf[0]; nx++){
            items[0] = m_xygrid[0][nx]*1000;
            for(int ny = 0; ny <= 2*m_nghalf[1]; ny++){
                items[1] = m_xygrid[1][ny]*1000;
                int nxy = nx+ny*(2*m_nghalf[0]+1);
                for(int n = 0; n < eppick.size(); n++){
                    items[2*n+2] = m_SxyGrid[0][nxy][eppick[n]];
                    items[2*n+3] = m_SxyGrid[1][nxy][eppick[n]];
                }
                PrintDebugItems(debug_out, items);
            }
        }
        debug_out.close();
    }
#endif

    if(!istime){
        return;
    }

    for(int nx = 0; nx <= 2*m_nghalf[0]; nx++){
        for(int ny = 0; ny <= 2*m_nghalf[1]; ny++){
            int nxy = nx+ny*(2*m_nghalf[0]+1);
            for(int n = 0; n < m_nfd; n++){
                for(int j = 0; j < 2; j++){
                    m_Fbuf[2*j][n] = m_SxyGrid[2*j][nxy][n];
                    m_Fbuf[2*j+1][n] = m_SxyGrid[2*j+1][nxy][n];
                }
            }
            f_GetTemporal();
            for(int n = -(int)m_nfft/2; n <= (int)m_nfft/2; n++){
                int idx = fft_index(n, m_nfft, -1);
                for(int j = 0; j < 2; j++){
                    m_EtGrid[nx][ny][j][n+(int)m_nfft/2] = m_EwFFT[j][idx]*coef;
                }
            }
        }
    }
    m_calcstatus->AdvanceStep(m_fellayer);

//---->>>
//#ifdef _DEBUG
    if(!FELTempProfile.empty()){
        ofstream debug_out(FELTempProfile);
        vector<string> titles(4);
        vector<double> items(4);
        titles[0] = "time(fs)";
        titles[1] = "x(mm)";
        titles[2] = "Ex";
        titles[3] = "Ey";
        PrintDebugItems(debug_out, titles);
        int ny = m_nghalf[1];
        for(int n = 0; n <= (int)m_nfft; n++){
            items[0] = m_tgrid[n]*1e15;
            //for(int nx = 0; nx <= 2*m_nghalf[0]; nx++){
            for(int nx = m_nghalf[0]; nx <= m_nghalf[0]; nx++){
                items[1] = m_xygrid[0][nx]*1000;
                for(int j = 0; j < 2; j++){
                    items[j+2] = m_EtGrid[nx][ny][j][n];
                }
                PrintDebugItems(debug_out, items);
            }
        }
        debug_out.close();
    }
//#endif
}

void FELAmplifier::f_GetComplexAmpMB(int tgtindex, double *xyobs)
{
    double bmlim[2] = {0, 0}, cutoff[2], xy[2], bdft[2];
    for(int j = 0; j < 2 && tgtindex < m_nsections-1; j++){
        bmlim[j] = m_bmsize[j][tgtindex+1]*m_gaussian_limit;
        // upper limit determined by the beam size at (tgtindex+1)-th section
    }

    //------->>>>>>
//    for(int nsec = 0; nsec <= tgtindex; nsec++){
    for(int nsec = tgtindex; nsec <= tgtindex; nsec++){
        for(int nx = 0; nx <= 2*m_nghalf[0]; nx++){
            xy[0] = m_xygrid[0][nx];
            for(int ny = 0; ny <= 2*m_nghalf[1]; ny++){
                xy[1] = m_xygrid[1][ny];
                bool isskip = tgtindex < m_nsections-1 && 
                    (fabs(xy[0]) > bmlim[0] || fabs(xy[1]) > bmlim[1]);
                if(!isskip){
                    for(int j = 0; j < 2 && xyobs != nullptr; j++){
                        xy[j] += xyobs[j];
                    }
                    f_GetComplexAmpSection(nsec, tgtindex, xy);
                }
                int nxy = nx+ny*(2*m_nghalf[0]+1);
                for(int n = 0; n < m_nfd; n++){
                    for(int i = 0; i < 2 && !isskip; i++){
                        bdft[i] = m_bunchf[nsec][i][n];
                    }
                    for(int j = 0; j < 2; j++){
                        if(isskip){
                            m_FxyGrid[2*j][nxy][n] = m_FxyGrid[2*j+1][nxy][n] = 0;
                        }
                        else{
                            m_FxyGrid[2*j][nxy][n] = m_Fxy[2*j][n]*bdft[0]-m_Fxy[2*j+1][n]*bdft[1];
                            m_FxyGrid[2*j+1][nxy][n] = m_Fxy[2*j][n]*bdft[1]+m_Fxy[2*j+1][n]*bdft[0];
                        }
                    }
                }
            }
        }
        for(int j = 0; j < 2; j++){
            cutoff[j] = m_dxy[j]/m_bmsize[j][nsec];
        }
        for(int j = 0; j < 2; j++){
            for(int n = 0; n < m_nfd; n++){
                for(int nx = 0; nx < m_ngfft[0]; nx++){
                    for(int ny = 0; ny < m_ngfft[1]; ny++){
                        int nxy = nx+ny*(2*m_nghalf[0]+1);
                        if(nx <= 2*m_nghalf[0] && ny <= 2*m_nghalf[1]){
                            m_ws[nx][2*ny] = m_FxyGrid[2*j][nxy][n];
                            m_ws[nx][2*ny+1] = m_FxyGrid[2*j+1][nxy][n];
                        }
                        else{
                            m_ws[nx][2*ny] = m_ws[nx][2*ny+1] = 0;
                        }
                    }
                }
                //---------->>>>>>>
                //m_spfft->DoFFTFilter2D(m_ws, cutoff, true);
                for(int nx = 0; nx <= 2*m_nghalf[0]; nx++){
                    for(int ny = 0; ny <= 2*m_nghalf[1]; ny++){
                        int nxy = nx+ny*(2*m_nghalf[0]+1);
                        m_SxyGrid[2*j][nxy][n] += m_ws[nx][2*ny];
                        m_SxyGrid[2*j+1][nxy][n] += m_ws[nx][2*ny+1];
                    }
                }
            }
        }
        m_calcstatus->AdvanceStep(m_fellayer);
    }
}

void FELAmplifier::f_GetComplexAmpSection(int srcindex, int tgtindex, double xy[])
{
    m_ntaupoints = m_secidx[1][srcindex]+1;
    if(m_ntaupoints > (int)m_tau.size()){
        for(int n = 0; n < m_nfd; n++){
            for(int j = 0; j < 2; j++){
                m_Fxy[2*j][n] = m_Fxy[2*j+1][n] = 0;
            }
        }
        return;
    }

    for(int j = 0; j < 2; j++){
        m_XYZ[j] = xy[j];
    }
    m_XYZ[2] = m_Zi[tgtindex];
    f_AllocateElectricField(false, true, true, false, &m_tstep[tgtindex]);
    int zrange[2];
    for(int j = 0; j < 2; j++){
        zrange[j] = m_secidx[j][srcindex];
    }
    f_AllocateComplexField(false, zrange, false, &m_tstep[tgtindex]);
}

// class SeedLight
SeedLight::SeedLight(double pkpower,
    double epcenter, double pulselenFWHM, double srcsizeFWHM,
    double zwaist, double torg)
{
    m_epcenter = epcenter;
    m_sigmat = pulselenFWHM/Sigma2FWHM;
    m_sigmath = m_sigmat/(PLANCK/PI2); // sigma_t/hbar
    m_sigmaxy = srcsizeFWHM/Sigma2FWHM;
    m_E0 = sqrt(pkpower*Z0VAC/PI)/m_sigmaxy; // W -> V/m
    m_Epk = m_E0*m_sigmat*m_sigmaxy*m_sigmaxy*4*pow(PI, 1.5);
    m_torg = torg;
    m_zwaist = zwaist;

    double kwave = PI2/wave_length(epcenter);
    m_zrayl = m_sigmaxy*2.0;
    m_zrayl *= m_zrayl*kwave/2.0;
}

void SeedLight::GetAmplitudeS(double ep, double tshift, double zpos, double xy[], double Exy[])
{
    if(ep <= 0){
        Exy[0] = Exy[1] = Exy[2] = Exy[3] = 0;
        return;
    }
    double kwave = PI2/wave_length(ep);
    double zrayl = m_sigmaxy*2.0;
    zrayl *= zrayl*kwave/2.0;
    double r2 = hypotsq(xy[0], xy[1]);
    zpos -= m_zwaist;
    double src2 = hypotsq(1, zpos/zrayl);
    double phase = -atan2(zpos, zrayl)+(tshift+m_torg)*CC*kwave;;
    if(fabs(zpos) > 0){
        phase += r2*kwave/zpos/hypotsq(1, zrayl/zpos)/2;
    }
    double tex = r2/(2*m_sigmaxy)/(2*m_sigmaxy)/src2;
    double eamp = m_E0*SQRTPI*m_sigmat/sqrt(src2)*f_GetAmp(ep, tex);
    Exy[0] = eamp*cos(phase);
    Exy[1] = eamp*sin(phase);
    Exy[2] = Exy[3] = 0;
}

void SeedLight::GetAmplitudeA(double ep,
    double tshift, double zpos, double kxy[], double Exy[])
{
    if(ep <= 0){
        Exy[0] = Exy[1] = Exy[2] = Exy[3] = 0;
        return;
    }
    double kwave = PI2/wave_length(ep);
    double tex = hypotsq(kxy[0]*m_sigmaxy, kxy[1]*m_sigmaxy);
    Exy[1] = 0; // imaginary = 0; waist position
    Exy[2] = Exy[3] = 0; // linear polarization
    if(tex > MAXIMUM_EXPONENT){
        Exy[0] = 0;
        return;
    }

    double eamp = f_GetAmp(ep, tex);
    double phase = (tshift+m_torg)*CC*kwave;
    phase -= (zpos-m_zwaist)/kwave*hypotsq(kxy[0], kxy[1])/2.0;
    Exy[0] = m_Epk*eamp*cos(phase);
    Exy[1] = m_Epk*eamp*sin(phase);
}

double SeedLight::f_GetAmp(double ep, double tex)
{
    double etexp = (ep+m_epcenter)*m_sigmath;
    etexp *= etexp;
    double etexm = (ep-m_epcenter)*m_sigmath;
    etexm *= etexm;
    double texp = tex+etexp;
    double texm = tex+etexm;
    double eamp = 0;
    if(texp < MAXIMUM_EXPONENT){
        eamp = exp(-texp);
    }
    if(texm < MAXIMUM_EXPONENT){
        eamp += exp(-texm);
    }
    return eamp;
}