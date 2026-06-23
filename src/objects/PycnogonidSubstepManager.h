#pragma once

#include "CoreMinimal.h"
#include "PycnogonidSubstepManager.generated.h"

// Thread-safe parameters updated by the main thread, read by the physics engine
struct FPycnogonidSubstepData
{
    float CurrentPH;
    float OptimalPH;
    float AlkalineK;
    float AlkalineExp;
    float AcidK;
    float AcidExp;
    float DeltaTime;
};

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class METASTASISTRACKERAI_API UPycnogonidSubstepManager : public UActorComponent
{
    GENERATED_BODY()

public:    
    UPycnogonidSubstepManager();

    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    // References to physics constraints that require thread-safe updates
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Physics Substep")
    TArray<class UPhysicsConstraintComponent*> TargetConstraints;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chemical Environment")
    float RunPH;

private:
    // Core callback signature hooked directly into the physics engine's substep loop
    void OnPhysicsSubstep(float SubstepDeltaTime, class FBodyInstance* BodyInstance);

    // Delegate handle to properly manage memory unregistration on shutdown
    FOnProcessPhysicsSubstep OnPhysicsSubstepDelegate;
    
    // Internal thread-safe cache mirror of structural integrity
    float SubstepStructuralIntegrity;
};
